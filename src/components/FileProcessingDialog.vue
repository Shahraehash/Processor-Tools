<template>
  <v-dialog
    v-model="isOpen"
  >
    <v-card class="text-center pa-10 loaders-transition">
      <v-progress-circular
        color="blue"
        size="160"
        width="15"
        indeterminate
        v-if="loading == true"
      >
        Processing
      </v-progress-circular>
      <div v-if="loading == false">


        <v-icon
          style="font-size:160px"
          class="loaders-transition"
          color="green"
        >mdi-check-circle-outline</v-icon>
        <div class="display-1">
          <v-icon x-large>mdi-arrow-down</v-icon>
          Your files are available below.
          <v-icon x-large>mdi-arrow-down</v-icon>
        </div>
        <div class="mt-5">
          <v-btn class="primary" @click="close()">Edit output</v-btn>
          <v-btn @click="home()">Exit tool</v-btn>
        </div>

      </div>



    </v-card>
  </v-dialog>


</template>
<script>
export default {
  name: 'X',
  props: ['isOpen','loading'],
  data() {
    return {
      methods: {
        close() {
          this.$store.commit('FileProcessingDialogOpenSet', false)
        },
        home() {
          this.$store.commit('FileProcessingDialogOpenSet', false)
          this.$router.push({name:'Landing'})

        }
      }

    }
  }
}
</script>
