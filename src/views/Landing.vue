<template>
  <v-container>
        <v-card
          class="my-5 pa-5 text-center"
          v-for="(data, name) in $store.state.tools" :key="name"
          hover
          outlined
          rounded
          @click="$router.push({name: name})"
          >
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
