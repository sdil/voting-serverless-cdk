<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        <h2 class="is-medium">{{ poll.question }}</h2>

        <ul>
          <li v-for="(count, answer) in poll.result"> {{ answer }} : {{ count }} </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    poll: {
      type: Object,
      required: true,
    },
  }
}
</script>