<template>
  <div>
    <div class="headline">
      <v-chip class="mt-n2" dark color="primary">{{stepNumber}}</v-chip>
      <span class="ml-2">{{stepTitle}}</span>
    </div>
  </div>
</template>
<script>
export default {
  name: 'StepHeading',
  props: ['stepNumber','stepTitle'],
  data() {
    return {
    }
  }
}
</script>
