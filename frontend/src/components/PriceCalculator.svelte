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

<div class="calculator">
  <div class="section-head">
    <span class="section-kicker">Tool 02</span>
    <h3>Price Calculator</h3>
    <p>
      คำนวณราคาขายจากต้นทุน USD, อัตราแลกเปลี่ยน, markup และ VAT
      เพื่อช่วยให้ทีมขายประเมินราคาได้เร็วขึ้น
    </p>
  </div>

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
    step="0.1"
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
    <div class="result-box">
      <div class="price-grid">
        <div>
          <span>ต้นทุนบาท</span>
          <strong>{formatNumber(priceResult.cost_thb)} บาท</strong>
        </div>

        <div>
          <span>ก่อน VAT</span>
          <strong>{formatNumber(priceResult.selling_price_before_vat)} บาท</strong>
        </div>

        <div>
          <span>VAT</span>
          <strong>{formatNumber(priceResult.vat_amount)} บาท</strong>
        </div>

        <div>
          <span>กำไรขั้นต้น</span>
          <strong>{formatNumber(priceResult.gross_profit)} บาท</strong>
        </div>
      </div>

      <div class="final-price">
        <span>ราคาขายสุทธิ</span>
        <strong>{formatNumber(priceResult.selling_price_final)} บาท</strong>
        <p>Margin: {priceResult.margin_percent.toFixed(2)}%</p>
      </div>
    </div>
  {/if}
</div>

<style>
  .calculator {
    min-width: 0;
  }

  .section-head h3 {
    font-size: clamp(26px, 3vw, 38px);
    margin-bottom: 8px;
  }

  .section-head p {
    max-width: 620px;
  }

  .price-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 16px;
  }

  .price-grid div {
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(30, 26, 23, 0.08);
    border-radius: 16px;
    padding: 14px;
  }

  .price-grid span,
  .final-price span {
    display: block;
    color: #6f655d;
    font-size: 13px;
    margin-bottom: 6px;
  }

  .price-grid strong {
    color: #1d1a17;
    font-size: 15px;
  }

  .final-price {
    border-radius: 18px;
    padding: 18px;
    background: #111;
    color: #fff;
  }

  .final-price strong {
    display: block;
    font-size: clamp(26px, 3vw, 38px);
    font-family: "Georgia", "Times New Roman", serif;
    font-weight: 500;
    color: #fff;
  }

  .final-price p {
    margin-top: 8px;
    color: rgba(255, 255, 255, 0.72);
  }

  @media (max-width: 640px) {
    .price-grid {
      grid-template-columns: 1fr;
    }
  }
</style>