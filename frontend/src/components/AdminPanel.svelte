<script>
  /**
   * @typedef {Object} Position
   * @property {number} id
   * @property {string} code
   * @property {string} name
   * @property {string | null} description
   */

  export let API_URL = "";

  /** @type {Position[]} */
  export let positions = [];

  /**
   * @type {() => void}
   */
  export let onDataChanged;

  let adminMessage = "";

  let newPositionCode = "";
  let newPositionName = "";
  let newPositionDescription = "";

  let newLessonPositionId = "";
  let newLessonTitle = "";
  let newLessonDescription = "";
  let newLessonStepOrder = 1;

  let newProductName = "";
  let newProductCategory = "";
  let newProductDiamondCarat = 0;
  let newProductDiamondCount = 0;
  let newProductMaterial = "";
  let newProductGoldType = "";
  let newProductGoldWeight = 0;
  let newProductDiamondColor = "";
  let newProductDiamondClarity = "";
  let newProductBarcode = "";
  let newProductCostCode = "";
  let newProductSellingPoint = "";

  async function createPosition() {
    adminMessage = "";

    const response = await fetch(`${API_URL}/positions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        code: newPositionCode,
        name: newPositionName,
        description: newPositionDescription
      })
    });

    if (response.ok) {
      adminMessage = "เพิ่มตำแหน่งงานสำเร็จ";
      newPositionCode = "";
      newPositionName = "";
      newPositionDescription = "";
      onDataChanged();
    } else {
      adminMessage = "เพิ่มตำแหน่งงานไม่สำเร็จ อาจมี code ซ้ำ";
    }
  }

  async function createLesson() {
    adminMessage = "";

    const response = await fetch(`${API_URL}/lessons`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        position_id: Number(newLessonPositionId),
        title: newLessonTitle,
        description: newLessonDescription,
        step_order: Number(newLessonStepOrder)
      })
    });

    if (response.ok) {
      adminMessage = "เพิ่มบทเรียนสำเร็จ";
      newLessonPositionId = "";
      newLessonTitle = "";
      newLessonDescription = "";
      newLessonStepOrder = 1;
      onDataChanged();
    } else {
      adminMessage = "เพิ่มบทเรียนไม่สำเร็จ";
    }
  }

  async function createProduct() {
    adminMessage = "";

    const response = await fetch(`${API_URL}/products`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: newProductName,
        category: newProductCategory,
        diamond_carat: Number(newProductDiamondCarat),
        diamond_count: Number(newProductDiamondCount),
        material: newProductMaterial,
        gold_type: newProductGoldType,
        gold_weight: Number(newProductGoldWeight),
        diamond_color: newProductDiamondColor,
        diamond_clarity: newProductDiamondClarity,
        barcode: newProductBarcode,
        cost_code: newProductCostCode,
        selling_point: newProductSellingPoint
      })
    });

    if (response.ok) {
      adminMessage = "เพิ่มสินค้าสำเร็จ";

      newProductName = "";
      newProductCategory = "";
      newProductDiamondCarat = 0;
      newProductDiamondCount = 0;
      newProductMaterial = "";
      newProductGoldType = "";
      newProductGoldWeight = 0;
      newProductDiamondColor = "";
      newProductDiamondClarity = "";
      newProductBarcode = "";
      newProductCostCode = "";
      newProductSellingPoint = "";

      onDataChanged();
    } else {
      adminMessage = "เพิ่มสินค้าไม่สำเร็จ อาจมี barcode ซ้ำ";
    }
  }
</script>

<section class="card admin-card">
  <p class="eyebrow">Admin Panel</p>
  <h2>เพิ่มข้อมูลเข้าระบบ</h2>
  <p>ใช้ส่วนนี้แทนการเพิ่มข้อมูลผ่าน FastAPI /docs</p>

  {#if adminMessage}
    <div class="admin-message">
      {adminMessage}
    </div>
  {/if}

  <div class="admin-grid">
    <div class="form-box">
      <h3>เพิ่มตำแหน่งงาน</h3>

      <label for="newPositionCode">Code</label>
      <input
        id="newPositionCode"
        bind:value={newPositionCode}
        placeholder="เช่น sales-store"
      />

      <label for="newPositionName">ชื่อตำแหน่ง</label>
      <input
        id="newPositionName"
        bind:value={newPositionName}
        placeholder="เช่น Sales หน้าร้าน"
      />

      <label for="newPositionDescription">รายละเอียด</label>
      <textarea
        id="newPositionDescription"
        bind:value={newPositionDescription}
        placeholder="รายละเอียดของตำแหน่งงาน"
      ></textarea>

      <button type="button" on:click={createPosition}>
        บันทึกตำแหน่งงาน
      </button>
    </div>

    <div class="form-box">
      <h3>เพิ่มบทเรียน</h3>

      <label for="newLessonPositionId">ตำแหน่งงาน</label>
      <select id="newLessonPositionId" bind:value={newLessonPositionId}>
        <option value="">เลือกตำแหน่งงาน</option>
        {#each positions as position}
          <option value={position.id}>{position.name}</option>
        {/each}
      </select>

      <label for="newLessonTitle">ชื่อบทเรียน</label>
      <input
        id="newLessonTitle"
        bind:value={newLessonTitle}
        placeholder="เช่น Step 1: พื้นฐานเครื่องประดับ"
      />

      <label for="newLessonDescription">รายละเอียดบทเรียน</label>
      <textarea
        id="newLessonDescription"
        bind:value={newLessonDescription}
        placeholder="รายละเอียดของบทเรียน"
      ></textarea>

      <label for="newLessonStepOrder">ลำดับ Step</label>
      <input
        id="newLessonStepOrder"
        type="number"
        bind:value={newLessonStepOrder}
      />

      <button type="button" on:click={createLesson}>
        บันทึกบทเรียน
      </button>
    </div>

    <div class="form-box product-form">
      <h3>เพิ่มสินค้า</h3>

      <label for="newProductName">ชื่อสินค้า</label>
      <input
        id="newProductName"
        bind:value={newProductName}
        placeholder="เช่น Diamond Ring Classic 18K"
      />

      <label for="newProductCategory">ประเภทสินค้า</label>
      <input
        id="newProductCategory"
        bind:value={newProductCategory}
        placeholder="เช่น Ring"
      />

      <label for="newProductDiamondCarat">น้ำหนักเพชร ct</label>
      <input
        id="newProductDiamondCarat"
        type="number"
        step="0.01"
        bind:value={newProductDiamondCarat}
      />

      <label for="newProductDiamondCount">จำนวนเพชร</label>
      <input
        id="newProductDiamondCount"
        type="number"
        bind:value={newProductDiamondCount}
      />

      <label for="newProductMaterial">วัสดุ</label>
      <input
        id="newProductMaterial"
        bind:value={newProductMaterial}
        placeholder="เช่น White Gold"
      />

      <label for="newProductGoldType">ประเภททอง</label>
      <input
        id="newProductGoldType"
        bind:value={newProductGoldType}
        placeholder="เช่น 18K"
      />

      <label for="newProductGoldWeight">น้ำหนักทอง g</label>
      <input
        id="newProductGoldWeight"
        type="number"
        step="0.01"
        bind:value={newProductGoldWeight}
      />

      <label for="newProductDiamondColor">Diamond Color</label>
      <input
        id="newProductDiamondColor"
        bind:value={newProductDiamondColor}
        placeholder="เช่น G"
      />

      <label for="newProductDiamondClarity">Diamond Clarity</label>
      <input
        id="newProductDiamondClarity"
        bind:value={newProductDiamondClarity}
        placeholder="เช่น VS"
      />

      <label for="newProductBarcode">Barcode</label>
      <input
        id="newProductBarcode"
        bind:value={newProductBarcode}
        placeholder="เช่น AFJ05018W"
      />

      <label for="newProductCostCode">Cost Code</label>
      <input
        id="newProductCostCode"
        bind:value={newProductCostCode}
        placeholder="เช่น AFJ"
      />

      <label for="newProductSellingPoint">จุดขายสินค้า</label>
      <textarea
        id="newProductSellingPoint"
        bind:value={newProductSellingPoint}
        placeholder="จุดขายที่พนักงานควรพูดกับลูกค้า"
      ></textarea>

      <button type="button" on:click={createProduct}>
        บันทึกสินค้า
      </button>
    </div>
  </div>
</section>

<style>
  .admin-card {
    border: 2px solid #d8c6ae;
  }

  h2 {
    margin-top: 0;
  }

  .admin-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 18px;
    align-items: start;
  }

  .form-box {
    background: #faf7f1;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #eee2d4;
  }

  .product-form {
    grid-column: span 2;
  }

  .form-box h3 {
    margin-top: 0;
  }

  .admin-message {
    margin-top: 18px;
    margin-bottom: 18px;
    padding: 16px;
    background: #f6f2eb;
    border-radius: 12px;
    border: 1px solid #d8c6ae;
    font-weight: bold;
  }

  @media (max-width: 768px) {
    .product-form {
      grid-column: span 1;
    }
  }
</style>