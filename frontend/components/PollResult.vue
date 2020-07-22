<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        <h2 class="is-medium">{{ question }}</h2>

        <ul>
          <li>Bird</li>
          <li>Plane</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {

    id: {
      type: String,
      required: true
    },
    question: {
      type: String,
      required: true
    }
  },
  data() {
    return {
        radio: 'default'
    }
  }
}
</script>