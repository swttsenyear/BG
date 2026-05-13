<script>
  /**
   * @typedef {Object} Position
   * @property {number} id
   * @property {string} code
   * @property {string} name
   * @property {string | null} description
   */

  /**
   * @typedef {Object} Lesson
   * @property {number} id
   * @property {number} position_id
   * @property {string} title
   * @property {string | null} description
   * @property {number} step_order
   * @property {boolean} is_active
   */

  export let API_URL = "";

  /** @type {Position | null} */
  export let selectedPosition = null;

  /** @type {Lesson[]} */
  export let lessons = [];

  /**
   * @type {() => void}
   */
  export let onDataChanged;

  /**
   * @param {Lesson} lesson
   */
  async function editLesson(lesson) {
    const newTitle = prompt("แก้ชื่อบทเรียน", lesson.title);
    if (newTitle === null) return;

    const newDescription = prompt("แก้รายละเอียดบทเรียน", lesson.description || "");
    if (newDescription === null) return;

    const newStepOrderText = prompt("แก้ลำดับ Step", String(lesson.step_order));
    if (newStepOrderText === null) return;

    const response = await fetch(`${API_URL}/lessons/${lesson.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title: newTitle,
        description: newDescription,
        step_order: Number(newStepOrderText)
      })
    });

    if (response.ok) {
      alert("แก้ไขบทเรียนสำเร็จ");
      onDataChanged();
    } else {
      alert("แก้ไขบทเรียนไม่สำเร็จ");
    }
  }

  /**
   * @param {Lesson} lesson
   */
  async function deleteLesson(lesson) {
    const confirmed = confirm(`ต้องการลบบทเรียน "${lesson.title}" ใช่ไหม?`);

    if (!confirmed) return;

    const response = await fetch(`${API_URL}/lessons/${lesson.id}`, {
      method: "DELETE"
    });

    if (response.ok) {
      alert("ลบบทเรียนสำเร็จ");
      onDataChanged();
    } else {
      alert("ลบบทเรียนไม่สำเร็จ");
    }
  }
</script>

{#if selectedPosition}
  <section class="card">
    <h2>Training Path: {selectedPosition.name}</h2>

    {#if lessons.length === 0}
      <p>ยังไม่มีบทเรียนของตำแหน่งนี้</p>
    {:else}
      <div class="lesson-list">
        {#each lessons as lesson}
          <div class="lesson-item">
            <div class="step-badge">{lesson.step_order}</div>

            <div class="lesson-content">
              <h3>{lesson.title}</h3>
              <p>{lesson.description}</p>

              <button
                type="button"
                class="secondary-button"
                on:click={() => editLesson(lesson)}
              >
                แก้ไข
              </button>

              <button
                type="button"
                class="danger-button"
                on:click={() => deleteLesson(lesson)}
              >
                ลบ
              </button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </section>
{/if}

<style>
  h2 {
    margin-top: 0;
  }

  .lesson-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .lesson-item {
    display: flex;
    gap: 16px;
    background: #faf7f1;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #eee2d4;
  }

  .lesson-content {
    flex: 1;
  }

  .step-badge {
    min-width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #2b2118;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }
</style>