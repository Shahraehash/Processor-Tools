<template>
  <v-container>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="resetStep1"
    />



  </v-container>

</template>

<script>
//packages


//support code

//components
import MenuBar from '@/components/MenuBar'


export default {
  name: 'Colinearity',
  components: {
    MenuBar,
  },
  props: [],
  created() {

  },
  data() {
    return {

    }
  },
  computed: {
    stepNumber() {
      if (this.showStep4) {
        return 4
      }
      else if (this.showStep3) {
        return 3
      }
      else if (this.showStep2) {
        return 2
      }
      else {
        return 1
      }
    },
    showStep2() {
      return false

    },
    showStep3() {
      return false

    },
    showStep4() {
      return false
    }


  },
  methods: {

    resetStep1() {
    },
    resetStep2() {
    },
    resetStep3() {
    },
    resetStep4() {

    },


  }
}
</script>
