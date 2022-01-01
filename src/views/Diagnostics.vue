<template>
  <v-container>
    <MenuBar
      title="Internal Diagnostics Tools"
      icon="mdi-gears"
      description="Internal QA Tools"
    />
    <v-card flat outlined class="ma-3 pa-3">
      <v-switch label="QA View" v-model="$store.state.diagnosticsEnabled"></v-switch>
    </v-card>

  </v-container>


</template>
<script>
//packages


//support code


//components
import MenuBar from '@/components/MenuBar'




export default {
  name:'Diagnostics',
  components: {
    MenuBar
  },
  data() {
    return {

    }
  }
}
</script>
<style>

</style>
