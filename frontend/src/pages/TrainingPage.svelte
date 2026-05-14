<script>
  import TrainingPath from "../components/TrainingPath.svelte";

  export let API_URL = "";

  /**
   * @type {{
   *   id: number,
   *   code: string,
   *   name: string,
   *   description: string | null
   * } | null}
   */
  export let selectedPosition = null;

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
  export let lessons = [];

  /**
   * @type {{
   *   name: string,
   *   employeeCode: string,
   *   role: string,
   *   roleLabel: string,
   *   position: {
   *     id: number,
   *     code: string,
   *     name: string,
   *     description: string | null
   *   }
   * } | null}
   */
  export let currentUser = null;

  /**
   * @type {{
   *   canViewDashboard: boolean,
   *   canViewTraining: boolean,
   *   canViewProducts: boolean,
   *   canViewTools: boolean,
   *   canViewAdmin: boolean,
   *   canManageProducts: boolean,
   *   canManageLessons: boolean,
   *   canViewCostCode: boolean,
   *   canUsePriceCalculator: boolean,
   *   canViewReports: boolean
   * }}
   */
  export let permissions = {
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

  /** @type {() => void} */
  export let onDataChanged = () => {};
</script>

<section class="page-block">
  <section class="training-user-bar">
    <div>
      <span class="section-kicker">Training Access</span>
      <h2>{currentUser?.name || "Unknown User"}</h2>
      <p>
        Role: <strong>{currentUser?.roleLabel || "-"}</strong>
        · Position: <strong>{selectedPosition?.name || "-"}</strong>
      </p>
    </div>
  </section>

  <TrainingPath
    {API_URL}
    {selectedPosition}
    {lessons}
    canManageLessons={permissions.canManageLessons}
    {onDataChanged}
  />
</section>

<style>
  .training-user-bar {
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(248, 246, 242, 0.92));
    border: 1px solid rgba(20, 20, 20, 0.08);
    border-radius: 32px;
    padding: clamp(24px, 3vw, 34px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.07);
  }

  .training-user-bar h2 {
    margin: 0 0 8px;
    font-size: clamp(34px, 4vw, 56px);
    line-height: 1.05;
  }

  .training-user-bar p {
    color: #6f655d;
    line-height: 1.7;
  }

  .training-user-bar strong {
    color: #1d1a17;
  }
</style>