<template>
      <v-btn
        @click="$emit('next')"
        class="primary"
        :disabled="disabled"
        :loading="loading"
        rounded
        text
        dark
        >
        {{text}}
      </v-btn>

</template>
<script>
export default {
  name: 'ButtonNext',
  props: ['action','disabled','text', 'loading'],
  watch: {
    loading: {
      handler: function (val) {
        console.log('loading state changed to: ' + val)
      },
      deep: true
    }
  },
  data() {
    return {
    }
  }
}
</script>
