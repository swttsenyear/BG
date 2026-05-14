<script>
  import BarcodeDecoder from "../components/BarcodeDecoder.svelte";
  import PriceCalculator from "../components/PriceCalculator.svelte";

  export let API_URL = "";
</script>

<section class="page-block">
  <section class="page-hero">
    <div class="hero-ghost">Barcode and pricing tools</div>

    <div class="page-hero-content">
      <span class="hero-eyebrow">Sales Tools</span>
      <h1 class="hero-title">Sales Utility Tools</h1>
      <p class="hero-subtitle">
        เครื่องมือช่วยพนักงานขายถอดรหัสต้นทุนและคำนวณราคาขายได้อย่างรวดเร็ว
        ลดความผิดพลาดจากการคำนวณด้วยมือ และช่วยให้ตอบลูกค้าได้มั่นใจมากขึ้น
      </p>
    </div>
  </section>

  <section class="section-card">
    <div class="section-head">
      <span class="section-kicker">Daily Operations</span>
      <h2 class="section-title">Barcode Decoder & Price Calculator</h2>
      <p class="section-description">
        ใช้งาน 2 เครื่องมือหลักสำหรับทีมขาย: ถอดรหัสต้นทุนจากตัวอักษร
        และคำนวณราคาขายจากต้นทุน USD, อัตราแลกเปลี่ยน, markup และ VAT
      </p>
    </div>

    <div class="grid-2">
      <div class="tool-card">
        <BarcodeDecoder {API_URL} />
      </div>

      <div class="tool-card">
        <PriceCalculator {API_URL} />
      </div>
    </div>
  </section>
</section>