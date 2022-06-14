<template>
  <v-container>
    <div v-for="(data, name) in $store.state.tools" :key="name">
      <v-card
        class="my-5 pa-5 text-center"
        hover
        outlined
        rounded
        v-if="data.isVisible"
        @click="$router.push({name: name})"
        >
        <v-icon x-large>{{data.icon}}</v-icon>
        
        <span class="title">{{data.title}}</span>
        <v-chip dark small color="blue" class="ml-3 mb-2" v-if="data.pro">MILO Pro</v-chip>
        <div class="caption">
          {{data.description}}
        </div>
      </v-card>

    </div>

  </v-container>
</template>
<script>
export default {
  name: 'Landing',
  data() {
    return {

    }
  },
  mounted() {
    this.$store.commit('FileProcessingDialogOpenSet', false)
  }
}
</script>
