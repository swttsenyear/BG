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

<section class="card">
  <h2>Barcode Decoder</h2>
  <p>ใส่รหัสต้นทุน เช่น AFJ เพื่อแปลงเป็นตัวเลข</p>

  <label for="barcodeCode">รหัสต้นทุน</label>
  <input
    id="barcodeCode"
    bind:value={code}
    placeholder="เช่น AFJ"
  />

  <button type="button" on:click={decodeBarcode}>ถอดรหัส</button>

  {#if decodeResult}
    <div class="result">
      <h3>ผลลัพธ์</h3>
      <p><strong>รหัส:</strong> {decodeResult.input_code}</p>
      <p><strong>ตัวเลข:</strong> {decodeResult.decoded_number}</p>

      {#each decodeResult.details as detail}
        <p>{detail}</p>
      {/each}
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