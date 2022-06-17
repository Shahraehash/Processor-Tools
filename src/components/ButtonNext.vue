<template>
    <div class="text-right" >
      <v-btn
        @click="action"
        class="primary"
        :disabled="disabled"
        rounded
        text
        dark
        >
        {{text}}
      </v-btn>
    </div>   
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
