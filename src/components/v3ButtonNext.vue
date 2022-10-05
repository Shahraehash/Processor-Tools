<template>
      <v-btn
        @click="$emit('next')"
        class="green"
        :disabled="disabled"
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
  props: ['action','disabled','text'],
  data() {
    return {
    }
  }
}
</script>
