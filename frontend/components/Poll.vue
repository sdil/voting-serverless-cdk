<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        <nuxt-link :to="'/poll/' + id">
          <h2 class="is-medium">{{ question }}</h2>
        </nuxt-link>

        <div class="field">
          <b-radio v-model="radio" native-value="bird">Bird</b-radio>
        </div>
        <div class="field">
          <b-radio v-model="radio" native-value="plane">Plane</b-radio>
        </div>

        <b-button type="is-dark">Submit</b-button>
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