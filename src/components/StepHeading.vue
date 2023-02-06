<template>
  <div class="mb-3">
    <div class="title primary--text">
      <v-chip class="mt-n1" dark color="primary">{{stepNumber}}</v-chip>
      <span class="ml-2">{{stepTitle}}</span>
    </div>
  </div>
</template>
<script>
export default {
  name: 'StepHeading',
  props: {
    stepNumber: {
        type: Number,
        default: () => '{{add stepNumber}}'
      },
      stepTitle: {
        type: String,
        default: () => '{{Add stepTitle}}'
      }
  },
  data() {
    return {
    }
  }
}
</script>
