<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        <h1 class="title is-large">Poll 1</h1>
        <h2 class="is-medium">What is that?</h2>

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
import Card from '~/components/Card'

export default {
  name: 'HomePage',

  components: {
    Card
  },
  data() {
    return {
        radio: 'default'
    }
  }

}
</script>
