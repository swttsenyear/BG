<script>
  export let API_URL = "";

  /**
   * @type {Array<{
   *   id: number,
   *   name: string,
   *   category: string | null,
   *   diamond_carat: number | null,
   *   diamond_count: number | null,
   *   material: string | null,
   *   gold_type: string | null,
   *   gold_weight: number | null,
   *   diamond_color: string | null,
   *   diamond_clarity: string | null,
   *   barcode: string | null,
   *   cost_code: string | null,
   *   selling_point: string | null
   * }>}
   */
  export let products = [];

  /** @type {() => void} */
  export let onDataChanged;

  const sampleImages = [
    "/brand/product-ring.jpg",
    "/brand/product-necklace.jpg",
    "/brand/product-earrings.jpg",
    "/brand/product-masterpiece.jpg"
  ];

  /**
   * @param {number} index
   */
  function getProductImage(index) {
    return sampleImages[index % sampleImages.length];
  }

  /**
   * @param {any} product
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
   * @param {any} product
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
      <div>◆</div>
      <h3>ยังไม่มีสินค้าในระบบ</h3>
      <p>เพิ่มสินค้าได้จากหน้า Admin</p>
    </div>
  {:else}
    <div class="product-grid">
      {#each products as product, index}
        <article class="product-card">
          <div
            class="product-visual"
            style={`background-image: linear-gradient(180deg, rgba(5,4,3,0.04), rgba(5,4,3,0.65)), url('${getProductImage(index)}')`}
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
    margin-bottom: 22px;
  }

  .section-title h2 {
    margin: 0;
    font-size: 32px;
    font-weight: normal;
  }

  .section-title span {
    background: #fffaf0;
    border: 1px solid rgba(201, 166, 70, 0.28);
    padding: 10px 14px;
    border-radius: 999px;
    color: #6c4e1f;
    font-weight: bold;
    font-family: Arial, sans-serif;
  }

  .product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
    gap: 24px;
  }

  .product-card {
    overflow: hidden;
    border-radius: 30px;
    background: #fffdf8;
    border: 1px solid rgba(201, 166, 70, 0.3);
    box-shadow: 0 18px 48px rgba(36, 26, 16, 0.1);
  }

  .product-visual {
    min-height: 260px;
    background-size: cover;
    background-position: center;
    color: #fffaf0;
    display: flex;
    align-items: flex-end;
    padding: 18px;
  }

  .product-visual span {
    background: rgba(5, 4, 3, 0.48);
    border: 1px solid rgba(234, 215, 154, 0.32);
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 12px;
    color: #fffaf0;
    font-family: Arial, sans-serif;
    backdrop-filter: blur(8px);
  }

  .product-body {
    padding: 24px;
  }

  .product-code {
    margin: 0 0 8px;
    color: #9b7625;
    letter-spacing: 1.5px;
    font-size: 11px;
    font-weight: bold;
    font-family: Arial, sans-serif;
  }

  .product-body h3 {
    margin: 0 0 18px;
    font-size: 25px;
    font-weight: normal;
  }

  .spec-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }

  .spec-grid div,
  .cost-box {
    background: #faf5e8;
    border: 1px solid #eee2d4;
    border-radius: 16px;
    padding: 13px;
  }

  .spec-grid span,
  .cost-box span {
    display: block;
    color: #8c7356;
    font-size: 12px;
    margin-bottom: 5px;
    font-family: Arial, sans-serif;
  }

  .spec-grid strong,
  .cost-box strong {
    color: #241a10;
    font-family: Arial, sans-serif;
  }

  .cost-box {
    margin-bottom: 16px;
  }

  .selling-point {
    background: white;
    border-left: 3px solid #c9a646;
    padding: 14px;
    border-radius: 14px;
    color: #5d4a39;
    line-height: 1.7;
    font-family: Arial, sans-serif;
  }

  .actions {
    margin-top: 16px;
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    background: #fffaf0;
    border-radius: 24px;
    border: 1px dashed rgba(201, 166, 70, 0.4);
  }

  .empty-state div {
    font-size: 60px;
    color: #c9a646;
  }

  .empty-state h3 {
    margin-bottom: 6px;
  }

  .empty-state p {
    color: #6c5a47;
  }
</style>