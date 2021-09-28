<template>
  <div>
    <v-alert :type="type" text dense>
      {{text}}
    </v-alert>

  </div>

</template>
<script>
export default {
  name: 'X',
  props: ['text', 'type'],
  data() {
    return {

    }
  }
}
</script>
