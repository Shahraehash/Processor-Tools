<template>
  <div class="text-center">
      <v-snackbar top
        :color="$store.state.snackbarMessage.color"
        :timeout="2000"
        v-model="$store.state.snackbarMessage.show"
        >
        {{$store.state.snackbarMessage.message}}
        <v-btn icon @click="$store.state.snackbarMessage.show = false"><v-icon>mdi-close</v-icon></v-btn>

      </v-snackbar>
  </div>

</template>
<script>
export default {
  name: 'MessageSnackbar',
  props: [
    'snackbar'
  ],
  watch: {
    show() {
      this.show = this.snackbar
    }
  },
  data() {
    return {
      show: false
    }
  }
}
</script>
