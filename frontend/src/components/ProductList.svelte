<script>
  /**
   * @typedef {Object} Product
   * @property {number} id
   * @property {string} name
   * @property {string | null} category
   * @property {number | null} diamond_carat
   * @property {number | null} diamond_count
   * @property {string | null} material
   * @property {string | null} gold_type
   * @property {number | null} gold_weight
   * @property {string | null} diamond_color
   * @property {string | null} diamond_clarity
   * @property {string | null} barcode
   * @property {string | null} cost_code
   * @property {string | null} selling_point
   */

  export let API_URL = "";
  export let canManageProducts = false;

  /** @type {Product[]} */
  export let products = [];

  /** @type {() => void} */
  export let onDataChanged = () => {};

  /**
   * @param {Product} product
   * @returns {string}
   */
  function getProductImage(product) {
    const name = (product.name || "").toLowerCase();
    const category = (product.category || "").toLowerCase();

    if (name.includes("brooch") || category.includes("brooch")) {
      return "/brand/product-masterpiece.JPG";
    }

    if (name.includes("necklace") || category.includes("necklace")) {
      return "/brand/product-necklace.jpg";
    }

    if (name.includes("earring") || category.includes("earring")) {
      return "/brand/product-earrings.jpg";
    }

    if (name.includes("ring") || category.includes("ring")) {
      return "/brand/product-ring.jpg";
    }

    return "/brand/product-masterpiece.JPG";
  }

  /**
   * @param {Product} product
   */
  async function editProduct(product) {
    const name = prompt("แก้ชื่อสินค้า", product.name);
    if (name === null) return;

    const category = prompt("แก้ประเภทสินค้า", product.category || "");
    if (category === null) return;

    const diamondCaratText = prompt("แก้น้ำหนักเพชร ct", String(product.diamond_carat || 0));
    if (diamondCaratText === null) return;

    const diamondCountText = prompt("แก้จำนวนเพชร", String(product.diamond_count || 0));
    if (diamondCountText === null) return;

    const material = prompt("แก้วัสดุ", product.material || "");
    if (material === null) return;

    const goldType = prompt("แก้ประเภททอง", product.gold_type || "");
    if (goldType === null) return;

    const goldWeightText = prompt("แก้น้ำหนักทอง g", String(product.gold_weight || 0));
    if (goldWeightText === null) return;

    const diamondColor = prompt("แก้ Diamond Color", product.diamond_color || "");
    if (diamondColor === null) return;

    const diamondClarity = prompt("แก้ Diamond Clarity", product.diamond_clarity || "");
    if (diamondClarity === null) return;

    const barcode = prompt("แก้ Barcode", product.barcode || "");
    if (barcode === null) return;

    const costCode = prompt("แก้ Cost Code", product.cost_code || "");
    if (costCode === null) return;

    const sellingPoint = prompt("แก้จุดขายสินค้า", product.selling_point || "");
    if (sellingPoint === null) return;

    const response = await fetch(`${API_URL}/products/${product.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name,
        category,
        diamond_carat: Number(diamondCaratText),
        diamond_count: Number(diamondCountText),
        material,
        gold_type: goldType,
        gold_weight: Number(goldWeightText),
        diamond_color: diamondColor,
        diamond_clarity: diamondClarity,
        barcode,
        cost_code: costCode,
        selling_point: sellingPoint
      })
    });

    if (response.ok) {
      alert("แก้ไขสินค้าสำเร็จ");
      onDataChanged();
    } else {
      alert("แก้ไขสินค้าไม่สำเร็จ อาจมี barcode ซ้ำ");
    }
  }

  /**
   * @param {Product} product
   */
  async function deleteProduct(product) {
    const confirmed = confirm(`ต้องการลบสินค้า "${product.name}" ใช่ไหม?`);
    if (!confirmed) return;

    const response = await fetch(`${API_URL}/products/${product.id}`, {
      method: "DELETE"
    });

    if (response.ok) {
      alert("ลบสินค้าสำเร็จ");
      onDataChanged();
    } else {
      alert("ลบสินค้าไม่สำเร็จ");
    }
  }
</script>

<section class="card">
  <div class="section-title">
    <div>
      <p class="eyebrow">Catalogue</p>
      <h2>High Jewelry Product Knowledge</h2>
    </div>

    <span>{products.length} items</span>
  </div>

  {#if products.length === 0}
    <div class="empty-state">
      <div>◇</div>
      <h3>ยังไม่มีสินค้าในระบบ</h3>
      <p>เพิ่มสินค้าได้จากหน้า Admin</p>
    </div>
  {:else}
    <div class="product-grid">
      {#each products as product}
        <article class="product-card">
          <div
            class="product-visual"
            style={`background-image: linear-gradient(180deg, rgba(5,5,5,0.02), rgba(5,5,5,0.45)), url('${getProductImage(product)}')`}
          >
            <span>{product.category || "High Jewelry"}</span>
          </div>

          <div class="product-body">
            <p class="product-code">{product.barcode || "NO BARCODE"}</p>
            <h3>{product.name}</h3>

            <div class="spec-grid">
              <div>
                <span>Carat</span>
                <strong>{product.diamond_carat || 0} ct</strong>
              </div>

              <div>
                <span>Diamonds</span>
                <strong>{product.diamond_count || 0}</strong>
              </div>

              <div>
                <span>Material</span>
                <strong>{product.material || "-"} {product.gold_type || ""}</strong>
              </div>

              <div>
                <span>Quality</span>
                <strong>{product.diamond_color || "-"} / {product.diamond_clarity || "-"}</strong>
              </div>
            </div>

            <div class="cost-box">
              <span>Cost Code</span>
              <strong>{product.cost_code || "-"}</strong>
            </div>

            <p class="selling-point">
              {product.selling_point || "ยังไม่มีจุดขายสินค้า"}
            </p>

            {#if canManageProducts}
              <div class="actions">
                <button
                  type="button"
                  class="secondary-button"
                  on:click={() => editProduct(product)}
                >
                  แก้ไข
                </button>

                <button
                  type="button"
                  class="danger-button"
                  on:click={() => deleteProduct(product)}
                >
                  ลบ
                </button>
              </div>
            {/if}
          </div>
        </article>
      {/each}
    </div>
  {/if}
</section>

<style>
  .section-title {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 18px;
    margin-bottom: 22px;
  }

  .section-title h2 {
    margin: 0;
    font-size: clamp(26px, 3vw, 36px);
    line-height: 1.12;
    font-weight: 400;
  }

  .section-title span {
    flex: 0 0 auto;
    background: #ffffff;
    border: 1px solid rgba(30, 30, 30, 0.08);
    padding: 10px 14px;
    border-radius: 999px;
    color: #5e1826;
    font-weight: 800;
    font-family: Arial, sans-serif;
  }

  .product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
  }

  .product-card {
    overflow: hidden;
    border-radius: 30px;
    background: #fff;
    border: 1px solid rgba(30, 30, 30, 0.08);
    box-shadow: 0 18px 48px rgba(0, 0, 0, 0.08);
    transition: all 0.24s ease;
  }

  .product-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 26px 70px rgba(0, 0, 0, 0.12);
  }

  .product-visual {
    height: 520px;
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    background-color: #101820;
    color: #fff;
    display: flex;
    align-items: flex-end;
    padding: 18px;
    overflow: hidden;
    position: relative;
  }

  .product-visual::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, transparent 65%, rgba(0,0,0,0.35));
  }

  .product-visual span {
    position: relative;
    z-index: 1;
    background: rgba(5, 5, 5, 0.52);
    border: 1px solid rgba(255, 255, 255, 0.18);
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 12px;
    color: #fff;
    font-family: Arial, sans-serif;
    backdrop-filter: blur(8px);
  }

  .product-body {
    padding: 24px;
  }

  .product-code {
    margin: 0 0 8px;
    color: #5e1826;
    letter-spacing: 1.7px;
    font-size: 11px;
    font-weight: 800;
    font-family: Arial, sans-serif;
  }

  .product-body h3 {
    margin: 0 0 18px;
    font-size: clamp(22px, 2.4vw, 28px);
    line-height: 1.15;
    font-weight: 400;
  }

  .spec-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }

  .spec-grid div,
  .cost-box {
    background: #f5f3ef;
    border: 1px solid rgba(30, 30, 30, 0.06);
    border-radius: 16px;
    padding: 13px;
  }

  .spec-grid span,
  .cost-box span {
    display: block;
    color: #6c625b;
    font-size: 12px;
    margin-bottom: 5px;
    font-family: Arial, sans-serif;
  }

  .spec-grid strong,
  .cost-box strong {
    color: #201b18;
    font-family: Arial, sans-serif;
  }

  .cost-box {
    margin-bottom: 16px;
  }

  .selling-point {
    background: #faf9f6;
    border-left: 3px solid #5e1826;
    padding: 14px;
    border-radius: 14px;
    color: #514943;
    line-height: 1.7;
    font-family: Arial, sans-serif;
  }

  .actions {
    margin-top: 16px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    background: #faf9f6;
    border-radius: 24px;
    border: 1px dashed rgba(30, 30, 30, 0.16);
  }

  .empty-state div {
    font-size: 60px;
    color: #5e1826;
  }

  .empty-state h3 {
    margin-bottom: 6px;
  }

  .empty-state p {
    color: #6c625b;
  }

  @media (max-width: 700px) {
    .section-title {
      flex-direction: column;
    }

    .product-grid {
      grid-template-columns: 1fr;
    }

    .spec-grid {
      grid-template-columns: 1fr;
    }

    .product-visual {
      height: 420px;
    }
  }
</style>