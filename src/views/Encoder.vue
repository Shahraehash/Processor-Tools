<template>
  <v-container>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="resetStep1"
    />



    <StepFileDrop
      stepTitle="File Selection"
      stepNumber="1"
      @files="batchEvaluateMetadataAndStore"
    />



  </v-container>

</template>

<script>
//packages


//support code
import FilePipeline from '@/FilePipeline.js'

//components
import MenuBar from '@/components/MenuBar'
import StepFileDrop from '@/components/v2/StepFileDrop'

export default {
  name: 'Encoder',
  components: {
    MenuBar,
    StepFileDrop
  },
  props: [],
  created() {

  },
  data() {
    return {
      filePipelines: [],
      toggle_exclusive: null

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
    //Step 1
    batchEvaluateMetadataAndStore(data) {
      let batch = []
      data.files.forEach(file => {
        let fp = FilePipeline.newFilePipeline()

        fp.file = file //associate original file
        fp.target = data.target //note the target

        //queue up processing
        batch.push(fp.evaluateMetadataAndStore())

        //store file pipeline
        this.filePipelines.push(fp)
      })
      Promise.all(batch).then(() => {
        console.log('done')
      })

    },

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
