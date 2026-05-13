<script>
  import PositionList from "../components/PositionList.svelte";
  import TrainingPath from "../components/TrainingPath.svelte";

  export let API_URL = "";

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
   * @type {(position: {
   *   id: number,
   *   code: string,
   *   name: string,
   *   description: string | null
   * }) => void}
   */
  export let onSelectPosition;

  /** @type {() => void} */
  export let onDataChanged;
</script>

<section class="page-hero">
  <p class="eyebrow">Training Academy</p>
  <h1>Build service excellence through structured learning.</h1>
  <p>
    เลือกตำแหน่งงานของพนักงาน แล้วระบบจะแสดงเส้นทางการสอนงานแบบ Step by Step
    เพื่อให้พนักงานใหม่เรียนรู้ได้เป็นมาตรฐานเดียวกัน
  </p>
</section>

<PositionList
  {API_URL}
  {positions}
  {onSelectPosition}
  {onDataChanged}
/>

<TrainingPath
  {API_URL}
  {selectedPosition}
  {lessons}
  {onDataChanged}
/>

<style>
  .page-hero {
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(255, 246, 225, 0.86)),
      radial-gradient(circle at top right, rgba(202, 167, 89, 0.22), transparent 34%);
    border: 1px solid rgba(202, 167, 89, 0.25);
    border-radius: 30px;
    padding: 30px;
    margin-bottom: 26px;
    box-shadow: 0 18px 50px rgba(36, 26, 16, 0.08);
  }

  .page-hero h1 {
    margin: 0 0 14px;
    font-size: 42px;
    font-weight: normal;
    max-width: 840px;
  }

  .page-hero p {
    color: #6c5a47;
    line-height: 1.8;
    max-width: 820px;
  }
</style>