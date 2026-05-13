<script>
  /**
   * @typedef {Object} PriceResult
   * @property {number} cost_usd
   * @property {number} exchange_rate
   * @property {number} markup
   * @property {number} vat_percent
   * @property {number} cost_thb
   * @property {number} selling_price_before_vat
   * @property {number} vat_amount
   * @property {number} selling_price_final
   * @property {number} gross_profit
   * @property {number} margin_percent
   */

  export let API_URL = "";

  let costUsd = 160;
  let exchangeRate = 36;
  let markup = 2.5;
  let vatPercent = 7;

  /** @type {PriceResult | null} */
  let priceResult = null;

  async function calculatePrice() {
    const response = await fetch(`${API_URL}/price/calculate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        cost_usd: Number(costUsd),
        exchange_rate: Number(exchangeRate),
        markup: Number(markup),
        vat_percent: Number(vatPercent)
      })
    });

    priceResult = await response.json();
  }

  /**
   * @param {number} number
   */
  function formatNumber(number) {
    return Number(number).toLocaleString("th-TH", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }
</script>

<section class="card">
  <h2>Price Calculator</h2>
  <p>คำนวณราคาจาก USD × ค่าเงิน × Markup + VAT</p>

  <label for="costUsd">ต้นทุน USD</label>
  <input
    id="costUsd"
    type="number"
    bind:value={costUsd}
  />

  <label for="exchangeRate">ค่าเงินบาท/USD</label>
  <input
    id="exchangeRate"
    type="number"
    bind:value={exchangeRate}
  />

  <label for="markup">Markup</label>
  <input
    id="markup"
    type="number"
    bind:value={markup}
  />

  <label for="vatPercent">VAT %</label>
  <input
    id="vatPercent"
    type="number"
    bind:value={vatPercent}
  />

  <button type="button" on:click={calculatePrice}>คำนวณราคา</button>

  {#if priceResult}
    <div class="result">
      <h3>ผลการคำนวณ</h3>
      <p><strong>ต้นทุนบาท:</strong> {formatNumber(priceResult.cost_thb)} บาท</p>
      <p><strong>ราคาก่อน VAT:</strong> {formatNumber(priceResult.selling_price_before_vat)} บาท</p>
      <p><strong>VAT:</strong> {formatNumber(priceResult.vat_amount)} บาท</p>
      <p><strong>ราคาขายสุทธิ:</strong> {formatNumber(priceResult.selling_price_final)} บาท</p>
      <p><strong>กำไรขั้นต้น:</strong> {formatNumber(priceResult.gross_profit)} บาท</p>
      <p><strong>Margin:</strong> {priceResult.margin_percent.toFixed(2)}%</p>
    </div>
  {/if}
</section>

<style>
  h2 {
    margin-top: 0;
  }

  .result {
    margin-top: 18px;
    padding: 16px;
    background: #f6f2eb;
    border-radius: 12px;
  }
</style>