<template>
  <v-alert dense text color="primary" class="ml-5">
    {{message}}
    <v-btn text v-if="decision != true" class="ml-3" @click="decide(true)">
      {{trueVal}}
    </v-btn>
    <v-btn text dark v-if="decision == true" color="primary" class="ml-3"  @click="decide(true)">
      {{trueVal}}
    </v-btn>
    <v-btn text v-if="decision != false" @click="decide(false)">
      {{falseVal}}
    </v-btn>
    <v-btn text dark v-if="decision == false" color="primary" @click="decide(false)">
      {{falseVal}}
    </v-btn>
  </v-alert>

</template>
<script>
export default {
  name: 'Decision',
  props: ['decision', 'trueVal', 'falseVal', 'message'],
  data() {
    return {

    }
  },
  methods: {
    decide(bool) {

      this.$emit('decide', bool)
    }
  }
}
</script>
