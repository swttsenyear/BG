<script>
  /**
   * @typedef {Object} DecodeResult
   * @property {string} input_code
   * @property {string} decoded_number
   * @property {string[]} details
   */

  export let API_URL = "";

  let code = "";

  /** @type {DecodeResult | null} */
  let decodeResult = null;

  async function decodeBarcode() {
    if (!code.trim()) return;

    const response = await fetch(`${API_URL}/barcode/decode`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        code: code
      })
    });

    decodeResult = await response.json();
  }
</script>

<div class="decoder">
  <div class="section-head">
    <span class="section-kicker">Tool 01</span>
    <h3>Barcode Decoder</h3>
    <p>
      ใส่รหัสต้นทุน เช่น AFJ เพื่อแปลงตัวอักษรเป็นตัวเลขที่ใช้ในการคำนวณต้นทุน
    </p>
  </div>

  <label for="barcodeCode">รหัสต้นทุน</label>
  <input
    id="barcodeCode"
    bind:value={code}
    placeholder="เช่น AFJ"
  />

  <button type="button" on:click={decodeBarcode}>ถอดรหัส</button>

  {#if decodeResult}
    <div class="result-box">
      <p><strong>รหัส:</strong> {decodeResult.input_code}</p>
      <p>
        <strong>ตัวเลข:</strong>
        <span class="metric">{decodeResult.decoded_number}</span>
      </p>

      <div class="detail-list">
        {#each decodeResult.details as detail}
          <span>{detail}</span>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .decoder {
    min-width: 0;
  }

  .section-head h3 {
    font-size: clamp(26px, 3vw, 38px);
    margin-bottom: 8px;
  }

  .section-head p {
    max-width: 620px;
  }

  .detail-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
  }

  .detail-list span {
    display: inline-flex;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(30, 26, 23, 0.08);
    font-size: 13px;
    color: #4d4540;
  }
</style>