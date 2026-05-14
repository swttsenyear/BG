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

<section class="page-block">
  <section class="page-hero">
    <div class="hero-ghost">Back office management</div>

    <div class="page-hero-content">
      <span class="hero-eyebrow">Admin Panel</span>
      <h1 class="hero-title">System Management</h1>
      <p class="hero-subtitle">
        จัดการข้อมูลตำแหน่งงาน บทเรียน และสินค้า
        เพื่อดูแลระบบฝึกอบรมให้พร้อมใช้งานและอัปเดตอยู่เสมอ
      </p>
    </div>
  </section>

  <AdminPanel
    {API_URL}
    {positions}
    {onDataChanged}
  />
</section>