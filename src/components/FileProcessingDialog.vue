<template>
  <v-dialog
    persistent
    v-model="isOpen"
  >
    <v-card class="text-center pa-10 loaders-transition">

        <div v-if="loading == true">
          <v-progress-circular
            color="blue"
            size="160"
            width="15"
            indeterminate
          >
            Processing
          </v-progress-circular>
          <v-alert 
          
            :style="{opacity: longProcessingTime}"
            class="mt-3"
            color="primary" 
            text
            >
            Large files can take much longer depending on the performance of your computer.
          </v-alert>    

        </div>


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
            <v-btn rounded text class="primary ma-2" @click="close()">Edit output</v-btn>
            <v-btn rounded outlined text class="ma-2" @click="home">Exit tool</v-btn>
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
      longProcessingTime: 0


    }
  },
  computed: {
    fileLoading() {
      return this.$store.state.fileProcessingDialog.loading

    },
  },
  watch: {
    fileLoading(newValue) {
      console.log(newValue, 'file watcher')
      if (newValue) {
        setTimeout(() => {this.longProcessingTime = 100}, 7000)
      }
      else {
        this.longProcessingTime = 0
      }

    }

  },
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
</script>
<style>
</style>
