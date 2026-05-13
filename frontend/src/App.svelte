<script>
  import DashboardPage from "./pages/DashboardPage.svelte";
  import TrainingPage from "./pages/TrainingPage.svelte";
  import ProductsPage from "./pages/ProductsPage.svelte";
  import ToolsPage from "./pages/ToolsPage.svelte";
  import AdminPage from "./pages/AdminPage.svelte";

  const API_URL = "http://127.0.0.1:8000";

  let currentPage = "dashboard";

  /**
   * @type {Array<{
   *   id: number,
   *   code: string,
   *   name: string,
   *   description: string | null
   * }>}
   */
  let positions = [];

  /**
   * @type {Array<{
   *   id: number,
   *   position_id: number,
   *   title: string,
   *   description: string | null,
   *   step_order: number,
   *   is_active: boolean
   * }>}
   */
  let lessons = [];

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
  let products = [];

  /**
   * @type {{
   *   id: number,
   *   code: string,
   *   name: string,
   *   description: string | null
   * } | null}
   */
  let selectedPosition = null;

  async function loadPositions() {
    const response = await fetch(`${API_URL}/positions`);
    positions = await response.json();
  }

  async function loadProducts() {
    const response = await fetch(`${API_URL}/products`);
    products = await response.json();
  }

  /**
   * @param {{
   *   id: number,
   *   code: string,
   *   name: string,
   *   description: string | null
   * }} position
   */
  async function loadLessonsByPosition(position) {
    selectedPosition = position;

    const response = await fetch(`${API_URL}/positions/${position.id}/lessons`);
    lessons = await response.json();
  }

  async function refreshAllData() {
    await loadPositions();
    await loadProducts();

    if (selectedPosition) {
      await loadLessonsByPosition(selectedPosition);
    }
  }

  /**
   * @param {string} page
   */
  function goTo(page) {
    currentPage = page;
  }

  loadPositions();
  loadProducts();
</script>

<div class="app-shell">
  <aside class="sidebar">
    <div class="brand">
      <div class="logo-frame">
        <img src="/brand/bg-logo.png" alt="Beauty Gems logo" />
      </div>

      <div class="brand-text">
        <p>Beauty Gems</p>
        <h1>Sales Academy</h1>
      </div>
    </div>

    <nav class="nav">
      <button class:active={currentPage === "dashboard"} on:click={() => goTo("dashboard")}>
        <span>01</span> Dashboard
      </button>

      <button class:active={currentPage === "training"} on:click={() => goTo("training")}>
        <span>02</span> Training
      </button>

      <button class:active={currentPage === "products"} on:click={() => goTo("products")}>
        <span>03</span> Products
      </button>

      <button class:active={currentPage === "tools"} on:click={() => goTo("tools")}>
        <span>04</span> Tools
      </button>

      <button class:active={currentPage === "admin"} on:click={() => goTo("admin")}>
        <span>05</span> Admin
      </button>
    </nav>

    <div class="sidebar-footer">
      <p>High Jewelry Training Portal</p>
      <small>Internal System / Version 0.6</small>
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div class="topbar-copy">
        <p class="eyebrow">Beauty Gems Internal Academy</p>
        <h2>
          {currentPage === "dashboard" ? "Luxury Sales Training Portal" : ""}
          {currentPage === "training" ? "Training Academy" : ""}
          {currentPage === "products" ? "High Jewelry Product Knowledge" : ""}
          {currentPage === "tools" ? "Sales Utility Tools" : ""}
          {currentPage === "admin" ? "Back Office Management" : ""}
        </h2>
      </div>

      <div class="status-pill">
        <span></span>
        API Online
      </div>
    </header>

    <section class="page-motion">
      {#if currentPage === "dashboard"}
        <DashboardPage
          {positions}
          {products}
          {lessons}
          onNavigate={goTo}
        />
      {/if}

      {#if currentPage === "training"}
        <TrainingPage
          {API_URL}
          {positions}
          {selectedPosition}
          {lessons}
          onSelectPosition={loadLessonsByPosition}
          onDataChanged={refreshAllData}
        />
      {/if}

      {#if currentPage === "products"}
        <ProductsPage
          {API_URL}
          {products}
          onDataChanged={refreshAllData}
        />
      {/if}

      {#if currentPage === "tools"}
        <ToolsPage {API_URL} />
      {/if}

      {#if currentPage === "admin"}
        <AdminPage
          {API_URL}
          {positions}
          onDataChanged={refreshAllData}
        />
      {/if}
    </section>
  </main>
</div>

<style>
  :global(*) {
    box-sizing: border-box;
  }

  :global(body) {
    margin: 0;
    min-height: 100vh;
    color: #201b18;
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
    background:
      radial-gradient(circle at 15% 10%, rgba(220, 225, 230, 0.42), transparent 28%),
      radial-gradient(circle at 88% 88%, rgba(94, 24, 38, 0.13), transparent 28%),
      linear-gradient(135deg, #080808 0%, #151515 34%, #f3f1ed 34%, #faf9f6 100%);
  }

  :global(h1),
  :global(h2),
  :global(h3) {
    font-family: "Georgia", "Times New Roman", serif;
    letter-spacing: -0.03em;
  }

  :global(p) {
    line-height: 1.75;
  }

  .app-shell {
    min-height: 100vh;
    display: grid;
    grid-template-columns: 300px minmax(0, 1fr);
  }

  .sidebar {
    height: 100vh;
    position: sticky;
    top: 0;
    padding: 28px 24px;
    background:
      linear-gradient(180deg, rgba(7, 7, 7, 0.98), rgba(24, 22, 21, 0.98)),
      radial-gradient(circle at top, rgba(205, 212, 218, 0.16), transparent 34%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    color: #f8f6f1;
    display: flex;
    flex-direction: column;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 42px;
    min-width: 0;
  }

  .logo-frame {
    width: 60px;
    height: 60px;
    flex: 0 0 auto;
    border-radius: 18px;
    background: #f8f6f1;
    border: 1px solid rgba(255, 255, 255, 0.42);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    overflow: hidden;
    box-shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
  }

  .logo-frame img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .brand-text {
    min-width: 0;
  }

  .brand p {
    margin: 0;
    color: #c9cdd2;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    font-size: 10px;
    font-weight: 700;
  }

  .brand h1 {
    margin: 4px 0 0;
    font-size: clamp(18px, 2vw, 23px);
    font-weight: 400;
    white-space: normal;
    line-height: 1.1;
  }

  .nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .nav button {
    width: 100%;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.035);
    color: #f8f6f1;
    padding: 14px 16px;
    border-radius: 16px;
    text-align: left;
    cursor: pointer;
    transition: all 0.22s ease;
    box-shadow: none;
    margin: 0;
  }

  .nav button span {
    color: #aeb4ba;
    margin-right: 12px;
    font-size: 11px;
    letter-spacing: 1px;
  }

  .nav button:hover,
  .nav button.active {
    background: #f8f6f1;
    color: #111;
    transform: translateX(4px);
  }

  .nav button:hover span,
  .nav button.active span {
    color: #5e1826;
  }

  .sidebar-footer {
    margin-top: auto;
    padding-top: 22px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .sidebar-footer p {
    margin: 0 0 6px;
    color: #f8f6f1;
    font-size: 13px;
  }

  .sidebar-footer small {
    color: #aeb4ba;
    font-size: 12px;
  }

  .main {
    min-width: 0;
    padding: 28px;
  }

  .topbar {
    min-height: 104px;
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(246, 245, 242, 0.84));
    border: 1px solid rgba(30, 30, 30, 0.08);
    border-radius: 28px;
    padding: 22px 26px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(18px);
  }

  .topbar-copy {
    min-width: 0;
  }

  .eyebrow,
  :global(.eyebrow) {
    margin: 0 0 8px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2.6px;
    color: #5e1826;
    font-weight: 800;
  }

  .topbar h2 {
    margin: 0;
    font-size: clamp(24px, 3vw, 34px);
    line-height: 1.12;
    font-weight: 400;
    color: #151515;
    overflow-wrap: anywhere;
  }

  .status-pill {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 10px 14px;
    border-radius: 999px;
    background: #ffffff;
    border: 1px solid rgba(30, 30, 30, 0.08);
    color: #333;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.05);
  }

  .status-pill span {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #2fbf71;
    box-shadow: 0 0 0 5px rgba(47, 191, 113, 0.13);
  }

  .page-motion {
    animation: fadeUp 0.45s ease both;
  }

  :global(.card) {
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(247, 246, 243, 0.9));
    border: 1px solid rgba(30, 30, 30, 0.08);
    border-radius: 28px;
    padding: clamp(20px, 3vw, 28px);
    margin-bottom: 24px;
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.07);
  }

  :global(.grid) {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 18px;
  }

  :global(input),
  :global(textarea),
  :global(select) {
    width: 100%;
    max-width: 620px;
    display: block;
    padding: 14px 15px;
    margin: 8px 0 16px;
    border-radius: 14px;
    border: 1px solid rgba(30, 30, 30, 0.12);
    background: rgba(255, 255, 255, 0.9);
    color: #201b18;
    outline: none;
  }

  :global(textarea) {
    min-height: 96px;
    resize: vertical;
  }

  :global(input:focus),
  :global(textarea:focus),
  :global(select:focus) {
    border-color: #5e1826;
    box-shadow: 0 0 0 4px rgba(94, 24, 38, 0.1);
  }

  :global(label) {
    display: block;
    margin-top: 12px;
    color: #201b18;
    font-weight: 700;
    font-size: 14px;
  }

  :global(button) {
    border: none;
    border-radius: 999px;
    padding: 12px 18px;
    margin-right: 8px;
    margin-top: 8px;
    cursor: pointer;
    color: #fff;
    background: #151515;
    font-weight: 700;
    box-shadow: 0 12px 26px rgba(0, 0, 0, 0.16);
    transition: all 0.22s ease;
  }

  :global(button:hover) {
    transform: translateY(-2px);
    background: #5e1826;
    box-shadow: 0 18px 34px rgba(94, 24, 38, 0.18);
  }

  :global(.secondary-button) {
    background: #f8f6f1;
    color: #151515;
    border: 1px solid rgba(30, 30, 30, 0.1);
  }

  :global(.secondary-button:hover) {
    background: #e9e6df;
    color: #151515;
  }

  :global(.danger-button) {
    background: #8e2b2b;
    color: white;
  }

  @keyframes fadeUp {
    from {
      opacity: 0;
      transform: translateY(14px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @media (max-width: 960px) {
    .app-shell {
      grid-template-columns: 1fr;
    }

    .sidebar {
      height: auto;
      position: relative;
    }

    .nav {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
    }

    .main {
      padding: 18px;
    }

    .topbar {
      flex-direction: column;
      align-items: flex-start;
    }
  }

  @media (max-width: 560px) {
    .nav {
      grid-template-columns: 1fr;
    }

    .brand {
      align-items: flex-start;
    }
  }
</style>