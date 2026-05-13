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

<section class="hero-card">
  <div class="hero-overlay">
    <p class="eyebrow">Beauty Gems Sales Academy</p>
    <h1>High jewelry knowledge, crafted into service excellence.</h1>
    <p>
      ระบบฝึกอบรมพนักงานขายเครื่องประดับระดับ High Jewelry
      รวมความรู้สินค้า บทเรียน วิธีอ่านรหัส และเครื่องมือคำนวณราคาไว้ในที่เดียว
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

  <div class="hero-panel">
    <div class="panel-line"></div>
    <p>Internal Training Portal</p>
    <h3>Product Knowledge · Sales Tools · Staff Academy</h3>
  </div>
</section>

<section class="stats-grid">
  <div class="stat-card">
    <p>Positions</p>
    <h2>{positions.length}</h2>
    <span>ตำแหน่งงานในระบบ</span>
  </div>

  <div class="stat-card">
    <p>Products</p>
    <h2>{products.length}</h2>
    <span>รายการสินค้า</span>
  </div>

  <div class="stat-card">
    <p>Lessons</p>
    <h2>{lessons.length}</h2>
    <span>บทเรียนที่โหลดล่าสุด</span>
  </div>
</section>

<section class="card">
  <p class="eyebrow">System Modules</p>
  <h2>Core Training Experience</h2>

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

<style>
  .hero-card {
    min-height: 500px;
    border-radius: 32px;
    margin-bottom: 24px;
    overflow: hidden;
    background:
      linear-gradient(90deg, rgba(5, 5, 5, 0.88), rgba(5, 5, 5, 0.48), rgba(5, 5, 5, 0.22)),
      url("/brand/hero-jewelry.jpg");
    background-size: cover;
    background-position: center;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 28px 80px rgba(0, 0, 0, 0.18);
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.8fr);
    align-items: end;
    gap: 24px;
    padding: clamp(24px, 4vw, 46px);
    position: relative;
  }

  .hero-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.18));
    pointer-events: none;
  }

  .hero-overlay,
  .hero-panel {
    position: relative;
    z-index: 1;
  }

  .hero-overlay {
    max-width: 760px;
    color: #f8f6f1;
  }

  .hero-overlay h1 {
    margin: 0 0 18px;
    font-size: clamp(38px, 5.4vw, 68px);
    line-height: 0.98;
    font-weight: 400;
    text-wrap: balance;
  }

  .hero-overlay p {
    max-width: 660px;
    color: #f1eee9;
    line-height: 1.85;
    font-size: clamp(14px, 1.5vw, 16px);
  }

  .hero-actions {
    margin-top: 24px;
  }

  .hero-panel {
    align-self: stretch;
    justify-self: end;
    width: min(100%, 360px);
    padding: 26px;
    border-radius: 28px;
    background: rgba(248, 246, 241, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.22);
    backdrop-filter: blur(18px);
    color: #f8f6f1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    animation: floatIn 0.7s ease both;
  }

  .panel-line {
    width: 72px;
    height: 1px;
    background: #f8f6f1;
    margin-bottom: 18px;
    opacity: 0.8;
  }

  .hero-panel p {
    margin: 0 0 8px;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 700;
  }

  .hero-panel h3 {
    margin: 0;
    font-size: clamp(22px, 2.4vw, 30px);
    line-height: 1.15;
    font-weight: 400;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 24px;
  }

  .stat-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(30, 30, 30, 0.08);
    border-radius: 26px;
    padding: 24px;
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.07);
    transition: all 0.22s ease;
  }

  .stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.1);
  }

  .stat-card p {
    margin: 0;
    color: #5e1826;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 800;
  }

  .stat-card h2 {
    margin: 10px 0 4px;
    font-size: clamp(36px, 4vw, 52px);
    line-height: 1;
    font-weight: 400;
  }

  .stat-card span {
    color: #6c625b;
  }

  .module-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }

  .module-grid button {
    text-align: left;
    border-radius: 24px;
    padding: 24px;
    background:
      linear-gradient(135deg, rgba(255,255,255,0.94), rgba(237,235,230,0.9));
    border: 1px solid rgba(30, 30, 30, 0.08);
    color: #201b18;
    box-shadow: none;
    min-height: 145px;
  }

  .module-grid button:hover {
    background: #151515;
    color: #fff;
  }

  .module-grid strong {
    display: block;
    font-size: 17px;
    margin-bottom: 10px;
  }

  .module-grid span {
    display: block;
    color: #6c625b;
    line-height: 1.6;
    font-weight: 400;
  }

  .module-grid button:hover span {
    color: #ddd;
  }

  @keyframes floatIn {
    from {
      opacity: 0;
      transform: translateY(18px) scale(0.98);
    }

    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  @media (max-width: 1100px) {
    .hero-card {
      grid-template-columns: 1fr;
    }

    .hero-panel {
      justify-self: start;
      width: 100%;
    }

    .module-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 700px) {
    .stats-grid,
    .module-grid {
      grid-template-columns: 1fr;
    }

    .hero-card {
      min-height: auto;
    }
  }
</style>