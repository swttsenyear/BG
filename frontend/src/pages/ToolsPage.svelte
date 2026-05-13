<script>
  import BarcodeDecoder from "../components/BarcodeDecoder.svelte";
  import PriceCalculator from "../components/PriceCalculator.svelte";

  export let API_URL = "";
</script>

<section class="page-hero">
  <p class="eyebrow">Sales Tools</p>
  <h1>Barcode and pricing tools for daily sales operation.</h1>
  <p>
    เครื่องมือช่วยพนักงานขายถอดรหัสต้นทุนและคำนวณราคาขายได้รวดเร็วขึ้น
    ลดความผิดพลาดในการคำนวณด้วยมือ
  </p>
</section>

<div class="tools-grid">
  <BarcodeDecoder {API_URL} />
  <PriceCalculator {API_URL} />
</div>

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

  .tools-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 26px;
  }

  @media (max-width: 960px) {
    .tools-grid {
      grid-template-columns: 1fr;
    }
  }
</style>