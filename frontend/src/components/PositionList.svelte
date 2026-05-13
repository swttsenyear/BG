<script>
  /**
   * @typedef {Object} Position
   * @property {number} id
   * @property {string} code
   * @property {string} name
   * @property {string | null} description
   */

  export let API_URL = "";

  /** @type {Position[]} */
  export let positions = [];

  /**
   * @type {(position: Position) => void}
   */
  export let onSelectPosition;

  /**
   * @type {() => void}
   */
  export let onDataChanged;

  /**
   * @param {Position} position
   */
  async function editPosition(position) {
    const newCode = prompt("แก้ Code", position.code);
    if (newCode === null) return;

    const newName = prompt("แก้ชื่อตำแหน่ง", position.name);
    if (newName === null) return;

    const newDescription = prompt("แก้รายละเอียด", position.description || "");
    if (newDescription === null) return;

    const response = await fetch(`${API_URL}/positions/${position.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        code: newCode,
        name: newName,
        description: newDescription
      })
    });

    if (response.ok) {
      alert("แก้ไขตำแหน่งงานสำเร็จ");
      onDataChanged();
    } else {
      alert("แก้ไขไม่สำเร็จ อาจมี code ซ้ำ");
    }
  }

  /**
   * @param {Position} position
   */
  async function deletePosition(position) {
    const confirmed = confirm(
      `ต้องการลบตำแหน่ง "${position.name}" ใช่ไหม?\nบทเรียนของตำแหน่งนี้จะถูกลบด้วย`
    );

    if (!confirmed) return;

    const response = await fetch(`${API_URL}/positions/${position.id}`, {
      method: "DELETE"
    });

    if (response.ok) {
      alert("ลบตำแหน่งงานสำเร็จ");
      onDataChanged();
    } else {
      alert("ลบไม่สำเร็จ");
    }
  }
</script>

<section class="card">
  <div class="section-head">
    <div>
      <h2>เลือกตำแหน่งงาน</h2>
      <p>ข้อมูลนี้ดึงมาจาก FastAPI และ PostgreSQL</p>
    </div>
  </div>

  {#if positions.length === 0}
    <p>ยังไม่มีตำแหน่งงานในระบบ ให้เพิ่มผ่าน Admin Panel ก่อน</p>
  {:else}
    <div class="grid">
      {#each positions as position}
        <div class="mini-card">
          <h3>{position.name}</h3>
          <p><strong>Code:</strong> {position.code}</p>
          <p>{position.description}</p>

          <button type="button" on:click={() => onSelectPosition(position)}>
            เริ่มเรียน
          </button>

          <button
            type="button"
            class="secondary-button"
            on:click={() => editPosition(position)}
          >
            แก้ไข
          </button>

          <button
            type="button"
            class="danger-button"
            on:click={() => deletePosition(position)}
          >
            ลบ
          </button>
        </div>
      {/each}
    </div>
  {/if}
</section>

<style>
  .section-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }

  h2 {
    margin-top: 0;
  }

  .mini-card {
    background: #faf7f1;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #eee2d4;
  }

  .mini-card h3 {
    margin-top: 0;
  }
</style>