<template>
  <v-container>
    <v-row class="mb-10">
      <v-col cols="2">
        <v-img
          src="https://milo-ml.com/wp-content/uploads/2021/02/logo.png"
        ></v-img>
      </v-col>
      <v-col cols="9">
        <v-card flat class="display-1 pt-3 grey--text text--darken-3">
          PREPROCESSING TOOLS
        </v-card>

      </v-col>

    </v-row>







        <v-card
          class="my-5 pa-5 text-center"
          v-for="(data, name) in $store.state.tools" :key="name"
          hover outlined rounded  @click="$router.push({name: name})">
          <v-icon x-large>{{data.icon}}</v-icon>
          <span class="title">{{data.title}}</span>
          <div class="caption">
            {{data.description}}
          </div>
        </v-card>



  </v-container>
</template>
<script>
export default {
  name: 'Landing',
  data() {
    return {

    }
  }
}
</script>
