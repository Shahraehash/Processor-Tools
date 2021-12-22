<template>
  <v-card
    class="ma-3 pa-3 text-center"
    flat
    outlined
  >
    <div>
      <v-icon x-large class="">{{icon}}</v-icon>
      <span class="title">{{title}}</span>
    </div>
    <div class="ma-3 caption">
      {{description}}
    </div>
    <v-row>
      <v-col
        cols="6"
        class="text-left"
      >
        <v-btn
          text
          @click="$router.push({name: 'Landing'})"
        >
          <v-icon>mdi-arrow-left</v-icon>
          Home
        </v-btn>

      </v-col>
      <v-col
        cols="6"
        class="text-right"
      >
        <v-btn
          text
          @click="resetTool"
        >
          <v-icon>mdi-restart</v-icon>
          Reset Tool
        </v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  name: 'MenuBar',
  props: ['title','icon','description'],
  data() {
    return {
    }
  },
  methods: {
    resetTool() {
      this.$emit('reset')
    }
  }
}
</script>
