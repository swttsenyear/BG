<script>
  import DashboardPage from "./pages/DashboardPage.svelte";
  import TrainingPage from "./pages/TrainingPage.svelte";
  import ProductsPage from "./pages/ProductsPage.svelte";
  import ToolsPage from "./pages/ToolsPage.svelte";
  import AdminPage from "./pages/AdminPage.svelte";

  /**
   * @typedef {Object} Position
   * @property {number} id
   * @property {string} code
   * @property {string} name
   * @property {string | null} description
   */

  /**
   * @typedef {Object} Lesson
   * @property {number} id
   * @property {number} position_id
   * @property {string} title
   * @property {string | null} description
   * @property {number} step_order
   * @property {boolean} is_active
   */

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

  /**
   * @typedef {Object} CurrentUser
   * @property {string} name
   * @property {string} employeeCode
   * @property {string} role
   * @property {string} roleLabel
   * @property {Position} position
   */

  /**
   * @typedef {Object} Permissions
   * @property {boolean} canViewDashboard
   * @property {boolean} canViewTraining
   * @property {boolean} canViewProducts
   * @property {boolean} canViewTools
   * @property {boolean} canViewAdmin
   * @property {boolean} canManageProducts
   * @property {boolean} canManageLessons
   * @property {boolean} canViewCostCode
   * @property {boolean} canUsePriceCalculator
   * @property {boolean} canViewReports
   */

  /** @typedef {keyof Permissions} PermissionKey */

  /**
   * @typedef {Object} AccessRole
   * @property {string} value
   * @property {string} label
   * @property {string} description
   */

  /**
   * @typedef {Object} NavItem
   * @property {string} id
   * @property {string} label
   * @property {string} number
   * @property {PermissionKey} permission
   */

  const API_URL = "http://127.0.0.1:8000";

  let currentPage = "dashboard";
  let isAuthenticated = false;

  let loginName = "";
  let loginEmployeeCode = "";
  let loginPositionId = "";
  let loginRole = "sales";

  /** @type {CurrentUser | null} */
  let currentUser = null;

  /** @type {Position[]} */
  let positions = [];

  /** @type {Lesson[]} */
  let lessons = [];

  /** @type {Product[]} */
  let products = [];

  /** @type {Position | null} */
  let selectedPosition = null;

  /** @type {AccessRole[]} */
  const accessRoles = [
    {
      value: "trainee",
      label: "Trainee",
      description: "พนักงานใหม่ เห็น Training และ Product Knowledge แบบอ่านอย่างเดียว"
    },
    {
      value: "sales",
      label: "Sales Staff",
      description: "พนักงานขาย เห็น Training, Products และ Tools"
    },
    {
      value: "supervisor",
      label: "Supervisor",
      description: "หัวหน้าทีมขาย เห็นภาพรวมและเครื่องมือสำหรับทีม"
    },
    {
      value: "admin",
      label: "Admin / Training Manager",
      description: "จัดการสินค้า บทเรียน ตำแหน่ง และข้อมูลหลังบ้าน"
    },
    {
      value: "owner",
      label: "Owner / Management",
      description: "ดูภาพรวมระดับผู้บริหาร เน้น Dashboard และ Reports"
    }
  ];

  /** @type {NavItem[]} */
  const navItems = [
    { id: "dashboard", label: "Dashboard", number: "01", permission: "canViewDashboard" },
    { id: "training", label: "Training", number: "02", permission: "canViewTraining" },
    { id: "products", label: "Products", number: "03", permission: "canViewProducts" },
    { id: "tools", label: "Tools", number: "04", permission: "canViewTools" },
    { id: "admin", label: "Admin", number: "05", permission: "canViewAdmin" }
  ];

  /**
   * @param {string} role
   * @returns {Permissions}
   */
  function getPermissions(role) {
    const base = {
      canViewDashboard: true,
      canViewTraining: true,
      canViewProducts: true,
      canViewTools: false,
      canViewAdmin: false,
      canManageProducts: false,
      canManageLessons: false,
      canViewCostCode: false,
      canUsePriceCalculator: false,
      canViewReports: false
    };

    if (role === "trainee") {
      return base;
    }

    if (role === "sales") {
      return {
        ...base,
        canViewTools: true,
        canUsePriceCalculator: true
      };
    }

    if (role === "supervisor") {
      return {
        ...base,
        canViewTools: true,
        canViewCostCode: true,
        canUsePriceCalculator: true,
        canViewReports: true
      };
    }

    if (role === "admin") {
      return {
        canViewDashboard: true,
        canViewTraining: true,
        canViewProducts: true,
        canViewTools: true,
        canViewAdmin: true,
        canManageProducts: true,
        canManageLessons: true,
        canViewCostCode: true,
        canUsePriceCalculator: true,
        canViewReports: true
      };
    }

    if (role === "owner") {
      return {
        ...base,
        canViewTools: true,
        canViewCostCode: true,
        canUsePriceCalculator: true,
        canViewReports: true
      };
    }

    return base;
  }

  /** @type {Permissions} */
  $: permissions = getPermissions(currentUser?.role || loginRole);

  /** @type {NavItem[]} */
  $: visibleNavItems = navItems.filter((item) => permissions[item.permission]);

  /** @type {Position | null} */
  $: loginPosition =
    positions.find((position) => String(position.id) === String(loginPositionId)) || null;

  /** @type {AccessRole} */
  $: selectedAccessRole =
    accessRoles.find((role) => role.value === loginRole) || accessRoles[1];

  async function loadPositions() {
    const response = await fetch(`${API_URL}/positions`);
    /** @type {Position[]} */
    const data = await response.json();
    positions = data;
  }

  async function loadProducts() {
    const response = await fetch(`${API_URL}/products`);
    /** @type {Product[]} */
    const data = await response.json();
    products = data;
  }

  /**
   * @param {Position} position
   */
  async function loadLessonsByPosition(position) {
    selectedPosition = position;

    const response = await fetch(`${API_URL}/positions/${position.id}/lessons`);
    /** @type {Lesson[]} */
    const data = await response.json();
    lessons = data;
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

  async function enterAcademy() {
    if (!loginName.trim()) {
      alert("กรุณากรอกชื่อพนักงาน");
      return;
    }

    if (!loginPosition) {
      alert("กรุณาเลือก Position");
      return;
    }

    currentUser = {
      name: loginName.trim(),
      employeeCode: loginEmployeeCode.trim(),
      role: loginRole,
      roleLabel: selectedAccessRole.label,
      position: loginPosition
    };

    await loadLessonsByPosition(loginPosition);

    isAuthenticated = true;
    currentPage = "training";
  }

  function switchUser() {
    isAuthenticated = false;
    currentUser = null;
    selectedPosition = null;
    lessons = [];
    currentPage = "dashboard";
  }

  loadPositions();
  loadProducts();
</script>

{#if !isAuthenticated}
  <section class="access-page">
    <div class="access-visual">
      <div class="access-logo-top">
        <img src="/brand/bg-logo.png" alt="Beauty Gems logo" />
      </div>

      <div class="access-visual-content">
        <span>Beauty Gems Sales Academy</span>
        <h1>Luxury Training Access</h1>
        <p>
          ระบบฝึกอบรมพนักงานขายเครื่องประดับแบบ Role-Based
          เลือกตัวตน ตำแหน่ง และสิทธิ์การใช้งานก่อนเข้าสู่ Academy
        </p>
      </div>
    </div>

    <div class="access-panel">
      <div class="access-header">
        <span>Secure Academy Portal</span>
        <h2>Enter Academy</h2>
        <p>
          กรอกข้อมูลพนักงาน เลือก Position และ Access Role
          เพื่อเข้าสู่หน้าที่เหมาะกับสิทธิ์ของผู้ใช้งาน
        </p>
      </div>

      <div class="access-form">
        <label for="loginName">Employee Name</label>
        <input
          id="loginName"
          bind:value={loginName}
          placeholder="เช่น Mint / Beam / Sales Team A"
        />

        <label for="loginEmployeeCode">Employee ID / Nickname</label>
        <input
          id="loginEmployeeCode"
          bind:value={loginEmployeeCode}
          placeholder="เช่น S001 หรือปล่อยว่างได้"
        />

        <label for="loginPosition">Position</label>
        <select id="loginPosition" bind:value={loginPositionId}>
          <option value="">-- Select Position --</option>
          {#each positions as position}
            <option value={String(position.id)}>
              {position.name} ({position.code})
            </option>
          {/each}
        </select>

        <label for="loginRole">Access Role</label>
        <select id="loginRole" bind:value={loginRole}>
          {#each accessRoles as role}
            <option value={role.value}>{role.label}</option>
          {/each}
        </select>

        <div class="role-preview">
          <span>Access Preview</span>
          <strong>{selectedAccessRole.label}</strong>
          <p>{selectedAccessRole.description}</p>

          {#if loginPosition}
            <div class="position-chip">
              Position: {loginPosition.name}
            </div>
          {/if}
        </div>

        <button type="button" class="enter-button" on:click={enterAcademy}>
          Enter Academy
        </button>
      </div>
    </div>
  </section>
{:else}
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

      <div class="user-card">
        <span>Current User</span>
        <strong>{currentUser?.name}</strong>
        <p>{currentUser?.roleLabel}</p>
        <small>{currentUser?.position.name}</small>
      </div>

      <nav class="nav">
        {#each visibleNavItems as item}
          <button
            type="button"
            class:active={currentPage === item.id}
            on:click={() => goTo(item.id)}
          >
            <span>{item.number}</span> {item.label}
          </button>
        {/each}
      </nav>

      <div class="sidebar-footer">
        <p>High Jewelry Training Portal</p>
        <button type="button" class="switch-button" on:click={switchUser}>
          Switch User
        </button>
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

        <div class="topbar-user">
          <div>
            <span>{currentUser?.roleLabel}</span>
            <strong>{currentUser?.name}</strong>
          </div>

          <div class="status-pill">
            <span></span>
            API Online
          </div>
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
            {selectedPosition}
            {lessons}
            {currentUser}
            {permissions}
            onDataChanged={refreshAllData}
          />
        {/if}

        {#if currentPage === "products"}
          <ProductsPage
            {API_URL}
            {products}
            canManageProducts={permissions.canManageProducts}
            onDataChanged={refreshAllData}
          />
        {/if}

        {#if currentPage === "tools" && permissions.canViewTools}
          <ToolsPage {API_URL} />
        {/if}

        {#if currentPage === "admin" && permissions.canViewAdmin}
          <AdminPage
            {API_URL}
            {positions}
            onDataChanged={refreshAllData}
          />
        {/if}
      </section>
    </main>
  </div>
{/if}

<style>
  .access-page {
    min-height: 100vh;
    display: grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(430px, 0.9fr);
    background:
      radial-gradient(circle at top left, rgba(95, 29, 43, 0.16), transparent 24%),
      linear-gradient(135deg, #070707 0%, #111 42%, #f6f3ef 42%, #faf8f5 100%);
  }

  .access-visual {
    position: relative;
    display: flex;
    align-items: flex-end;
    padding: clamp(34px, 5vw, 70px);
    background:
      linear-gradient(90deg, rgba(5, 5, 5, 0.9), rgba(5, 5, 5, 0.45), rgba(5, 5, 5, 0.2)),
      url("/brand/hero-jewelry.jpg");
    background-size: cover;
    background-position: center;
    color: white;
  }
  .access-logo-top {
    position: absolute;
    top: 42px;
    left: 42px;
    z-index: 5;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    background: transparent;
    border: none;
    box-shadow: none;
    backdrop-filter: none;
  }

  .access-logo-top img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  .access-visual::after {
    content: "";
    position: absolute;
    inset: 0;
    background:
      radial-gradient(circle at 22% 18%, rgba(255,255,255,0.22), transparent 20%),
      linear-gradient(180deg, transparent, rgba(0,0,0,0.32));
    pointer-events: none;
  }

  .access-visual-content {
    position: relative;
    z-index: 2;
    max-width: 760px;
  }

  .access-visual-content span,
  .access-header span,
  .role-preview span,
  .user-card span,
  .topbar-user span {
    display: block;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  .access-visual-content span {
    color: rgba(255,255,255,0.7);
  }

  .access-visual-content h1 {
    margin: 0 0 18px;
    font-size: clamp(48px, 6vw, 86px);
    line-height: 0.95;
    color: white;
    font-weight: 500;
  }

  .access-visual-content p {
    max-width: 650px;
    color: rgba(255,255,255,0.82);
    line-height: 1.9;
    font-size: 17px;
  }

  .access-panel {
    padding: clamp(28px, 4vw, 56px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    background:
      radial-gradient(circle at top right, rgba(95,29,43,0.07), transparent 30%),
      linear-gradient(135deg, rgba(255,255,255,0.96), rgba(247,245,241,0.92));
  }

  .access-header {
    margin-bottom: 26px;
  }

  .access-header span {
    color: #5f1d2b;
  }

  .access-header h2 {
    margin: 0 0 12px;
    font-size: clamp(38px, 4vw, 62px);
    line-height: 1.02;
    font-weight: 500;
  }

  .access-header p {
    color: #6f655d;
    line-height: 1.85;
    max-width: 620px;
  }

  .access-form {
    padding: 28px;
    border-radius: 30px;
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(20,20,20,0.08);
    box-shadow: 0 24px 70px rgba(0,0,0,0.08);
  }

  .role-preview {
    margin: 8px 0 18px;
    padding: 20px;
    border-radius: 24px;
    background: #111;
    color: white;
  }

  .role-preview span {
    color: rgba(255,255,255,0.58);
  }

  .role-preview strong {
    display: block;
    font-family: Georgia, serif;
    font-size: 30px;
    font-weight: 500;
    margin-bottom: 8px;
  }

  .role-preview p {
    color: rgba(255,255,255,0.72);
    line-height: 1.7;
  }

  .position-chip {
    display: inline-flex;
    margin-top: 14px;
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 13px;
  }

  .enter-button {
    width: 100%;
    min-height: 58px;
    font-size: 16px;
  }

  .app-shell {
    min-height: 100vh;
    display: grid;
    grid-template-columns: 310px minmax(0, 1fr);
  }

  .sidebar {
    height: 100vh;
    position: sticky;
    top: 0;
    padding: 28px 24px;
    background: linear-gradient(180deg, rgba(7, 7, 7, 0.98), rgba(24, 22, 21, 0.98));
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    color: #f8f6f1;
    display: flex;
    flex-direction: column;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 24px;
    min-width: 0;
  }

  .logo-frame {
    width: 60px;
    height: 60px;
    flex: 0 0 auto;
    border-radius: 18px;
    background: #f8f6f1;
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
    font-size: 23px;
    font-weight: 400;
    line-height: 1.1;
  }

  .user-card {
    padding: 18px;
    border-radius: 24px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 24px;
  }

  .user-card span {
    color: rgba(255,255,255,0.54);
  }

  .user-card strong {
    display: block;
    font-size: 24px;
    line-height: 1.2;
    margin-bottom: 6px;
  }

  .user-card p {
    margin: 0 0 6px;
    color: rgba(255,255,255,0.78);
  }

  .user-card small {
    color: rgba(255,255,255,0.54);
  }

  .nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .nav button {
    width: 100%;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.035);
    color: #f8f6f1;
    padding: 14px 16px;
    border-radius: 16px;
    text-align: left;
    cursor: pointer;
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
    border-top: 1px solid rgba(255,255,255,0.1);
  }

  .sidebar-footer p {
    margin: 0 0 12px;
    color: #f8f6f1;
    font-size: 13px;
  }

  .switch-button {
    width: 100%;
    background: rgba(255,255,255,0.08);
    color: white;
    box-shadow: none;
  }

  .switch-button:hover {
    background: white;
    color: #111;
  }

  .main {
    min-width: 0;
    padding: 28px;
  }

  .topbar {
    min-height: 104px;
    background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(246,245,242,0.86));
    border: 1px solid rgba(30,30,30,0.08);
    border-radius: 28px;
    padding: 22px 26px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    box-shadow: 0 24px 70px rgba(0,0,0,0.08);
  }

  .eyebrow {
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
  }

  .topbar-user {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .topbar-user span {
    margin-bottom: 4px;
    color: #5e1826;
    font-size: 10px;
  }

  .topbar-user strong {
    font-size: 15px;
  }

  .status-pill {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 10px 14px;
    border-radius: 999px;
    background: #ffffff;
    border: 1px solid rgba(30,30,30,0.08);
    color: #333;
    font-size: 13px;
    font-weight: 700;
  }

  .status-pill span {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #2fbf71;
    box-shadow: 0 0 0 5px rgba(47,191,113,0.13);
  }

  @media (max-width: 1080px) {
    .access-page {
      grid-template-columns: 1fr;
    }

    .access-visual {
      min-height: 420px;
    }

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

    .topbar {
      flex-direction: column;
      align-items: flex-start;
    }
  }

  @media (max-width: 640px) {
    .access-logo-top {
      top: 24px !important;
      left: 24px !important;
      width: 90px !important;
      height: 90px !important;
      border-radius: 0 !important;
      background: transparent !important;
      box-shadow: none !important;
      padding: 0 !important;
    }
    .access-panel,
    .access-visual {
      padding: 24px;
    }

    .access-form {
      padding: 20px;
    }

    .main {
      padding: 18px;
    }

    .nav {
      grid-template-columns: 1fr;
    }
  }
  /* FORCE REMOVE LOGIN LOGO FRAME */
.access-logo-top {
  position: absolute !important;
  top: 42px !important;
  left: 42px !important;
  z-index: 5 !important;

  width: 120px !important;
  height: 120px !important;

  display: flex !important;
  align-items: center !important;
  justify-content: center !important;

  background: transparent !important;
  border: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  padding: 0 !important;
  overflow: visible !important;
}

.access-logo-top img {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;

  background: transparent !important;
  border: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
}
</style>