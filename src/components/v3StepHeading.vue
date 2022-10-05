<template>
    <div class="mb-3">
      <div class="title primary--text">
        <div style="display: inline" class="text-h4 title-oval">{{stepNumber}}</div>
        <span class="ml-1 text-h5"> {{stepTitle}}</span>
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
  <style scoped>
  .title-oval {

    background: #1976d2;
    padding: 0 20px;
    border-radius: 200px;;
    color: white;
  }

  </style>
  