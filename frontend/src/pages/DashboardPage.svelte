<script>
  /**
   * @type {Array<{
   *   id: number,
   *   code: string,
   *   name: string,
   *   description: string | null
   * }>}
   */
  export let positions = [];

  /**
   * @type {Array<{
   *   id: number,
   *   name: string
   * }>}
   */
  export let products = [];

  /**
   * @type {Array<{
   *   id: number,
   *   title: string
   * }>}
   */
  export let lessons = [];

  /** @type {(page: string) => void} */
  export let onNavigate;
</script>

<section class="page-block">
  <section class="page-hero hero-image">
    <div class="hero-ghost">Luxury sales academy</div>

    <div class="page-hero-content">
      <span class="hero-eyebrow">Beauty Gems Internal Academy</span>
      <h1 class="hero-title">Luxury Sales Training Portal</h1>
      <p class="hero-subtitle">
        ศูนย์กลางสำหรับการฝึกอบรมพนักงานขายเครื่องประดับระดับลักชัวรี
        ครอบคลุม product knowledge, sales tools และ training path ในระบบเดียว
      </p>

      <div class="hero-actions">
        <button type="button" on:click={() => onNavigate("training")}>
          Start Training
        </button>

        <button type="button" class="secondary-button" on:click={() => onNavigate("products")}>
          View Products
        </button>
      </div>
    </div>
  </section>

  <section class="grid-3">
    <div class="stat-card">
      <span>Positions</span>
      <strong>{positions.length}</strong>
      <p>ตำแหน่งงานในระบบ</p>
    </div>

    <div class="stat-card">
      <span>Products</span>
      <strong>{products.length}</strong>
      <p>รายการสินค้า</p>
    </div>

    <div class="stat-card">
      <span>Lessons</span>
      <strong>{lessons.length}</strong>
      <p>บทเรียนที่โหลดล่าสุด</p>
    </div>
  </section>

  <section class="section-card">
    <div class="section-head">
      <span class="section-kicker">System Modules</span>
      <h2 class="section-title">Core Training Experience</h2>
      <p class="section-description">
        เลือกเมนูที่ต้องการเพื่อเริ่มใช้งานระบบฝึกอบรม ทั้งบทเรียนสินค้า เครื่องมือขาย
        และระบบจัดการหลังบ้าน
      </p>
    </div>

    <div class="module-grid">
      <button type="button" on:click={() => onNavigate("training")}>
        <strong>Training Academy</strong>
        <span>เรียนรู้ตามตำแหน่งงานแบบ Step by Step</span>
      </button>

      <button type="button" on:click={() => onNavigate("products")}>
        <strong>Product Knowledge</strong>
        <span>คลังข้อมูลสินค้า เพชร วัสดุ และจุดขาย</span>
      </button>

      <button type="button" on:click={() => onNavigate("tools")}>
        <strong>Sales Tools</strong>
        <span>ถอดรหัสต้นทุนและคำนวณราคาขาย</span>
      </button>

      <button type="button" on:click={() => onNavigate("admin")}>
        <strong>Admin Management</strong>
        <span>เพิ่มและจัดการข้อมูลในระบบ</span>
      </button>
    </div>
  </section>
</section>

<style>
  .hero-image {
    min-height: 440px;
    display: flex;
    align-items: flex-end;
    background:
      linear-gradient(90deg, rgba(10, 10, 10, 0.86), rgba(10, 10, 10, 0.45), rgba(10, 10, 10, 0.18)),
      url("/brand/hero-jewelry.jpg");
    background-size: cover;
    background-position: center;
    color: #fff;
  }

  .hero-image .hero-title,
  .hero-image .hero-subtitle {
    color: #fff;
  }

  .hero-image .hero-subtitle {
    color: rgba(255, 255, 255, 0.86);
  }

  .hero-image .hero-ghost {
    color: rgba(255, 255, 255, 0.06);
  }

  .hero-actions {
    margin-top: 24px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .stat-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(30, 26, 23, 0.08);
    border-radius: 26px;
    padding: 24px;
    box-shadow: var(--shadow);
    transition: 0.22s ease;
  }

  .stat-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-hover);
  }

  .stat-card span {
    display: block;
    color: var(--accent);
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
  }

  .stat-card strong {
    display: block;
    font-family: "Georgia", "Times New Roman", serif;
    font-size: clamp(40px, 4vw, 58px);
    line-height: 1;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 8px;
  }

  .module-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
  }

  .module-grid button {
    min-height: 150px;
    text-align: left;
    border-radius: 24px;
    padding: 22px;
    background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(237,235,230,0.9));
    border: 1px solid rgba(30, 26, 23, 0.08);
    color: var(--text);
    box-shadow: none;
  }

  .module-grid button:hover {
    background: #151515;
    color: #fff;
  }

  .module-grid strong {
    display: block;
    margin-bottom: 10px;
    font-size: 17px;
  }

  .module-grid span {
    display: block;
    color: #6c625b;
    line-height: 1.65;
    font-weight: 400;
  }

  .module-grid button:hover span {
    color: #ddd;
  }

  @media (max-width: 1100px) {
    .module-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 640px) {
    .hero-image {
      min-height: 380px;
    }

    .module-grid {
      grid-template-columns: 1fr;
    }
  }
</style>