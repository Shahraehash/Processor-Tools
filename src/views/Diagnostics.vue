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

    <v-card>
      <v-btn @click="getRouteList()">Get Routes</v-btn>
      <v-card v-for="(item, key) in routes" :key="key">
        {{item}}
      </v-card>
    </v-card>

  </v-container>


</template>
<script>
//packages
import axios from 'axios'

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
      routes: []

    }
  },
  methods: {
    getRouteList() {
      return axios.post('/preprocessor_api/route_map', {
          headers: {
          'Content-Type': 'application/json',
          }
      }).then(response => {
        this.routes = response.data
        return response.data
      }).catch(error => {
        return error
      })



    }
  }
}
</script>
<style>

</style>
