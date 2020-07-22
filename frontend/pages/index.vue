<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        
        <Poll id="1" question="What is that?" />

        <Poll id="2" question="Where is that?" />

      </div>
    </div>
  </section>
</template>

<script>
import Poll from '~/components/Poll'

export default {
  name: 'HomePage',

  components: {
    Poll
  },
  data() {
    return {
        radio: 'default'
    }
  }

}
</script>
