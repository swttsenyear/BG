<script>
  import AdminPanel from "../components/AdminPanel.svelte";

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

  /** @type {() => void} */
  export let onDataChanged;
</script>

<section class="page-hero">
  <p class="eyebrow">Back Office</p>
  <h1>Manage training content and product knowledge.</h1>
  <p>
    ใช้หน้านี้สำหรับเพิ่มตำแหน่งงาน บทเรียน และสินค้าเข้าสู่ระบบ
    ข้อมูลทั้งหมดจะถูกบันทึกลง PostgreSQL
  </p>
</section>

<AdminPanel
  {API_URL}
  {positions}
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