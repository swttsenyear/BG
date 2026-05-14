<script>
  import ProductList from "../components/ProductList.svelte";

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

  export let canManageProducts = false;

  /** @type {() => void} */
  export let onDataChanged = () => {};
</script>

<section class="page-block">
  <section class="page-hero">
    <div class="hero-ghost">Product knowledge</div>

    <div class="page-hero-content">
      <span class="hero-eyebrow">Catalogue</span>
      <h1 class="hero-title">High Jewelry Products</h1>
      <p class="hero-subtitle">
        รวมข้อมูลสินค้า วัสดุ น้ำหนักเพชร จำนวนเพชร คุณภาพ และ selling point
        เพื่อช่วยให้ทีมขายเข้าใจสินค้าและสื่อสารกับลูกค้าได้อย่างมืออาชีพ
      </p>
    </div>
  </section>

  <ProductList
    {API_URL}
    {products}
    {canManageProducts}
    {onDataChanged}
  />
</section>