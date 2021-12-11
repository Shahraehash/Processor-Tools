<template>
  <v-container>
    <v-card outlined rounded class="pa-3 text-center display-1">
      Milo Preprocessing Tools
    </v-card>

    <v-row wrap>
      <v-col cols="6" class="mt-3">
        <v-card hover outlined rounded class="pa-3 text-center" @click="$router.push({name: 'ColumnReducer'})">
          <v-icon x-large>mdi-table-column-width</v-icon>
          <span class="title">Column Reducer Tool</span>
        </v-card>
      </v-col>
      <v-col cols="6" class="mt-3">
        <v-card hover outlined rounded class="pa-3 text-center" @click="$router.push({name: 'TrainTestSplit'})">
          <v-icon x-large>mdi-call-split</v-icon>
          <span class="title">Train and Test Builder</span>
        </v-card>
      </v-col>
      <v-col cols="6" class="mt-3">
        <v-card hover outlined rounded class="pa-3 text-center" @click="$router.push({name: 'Colinearity'})">
          <v-icon x-large>mdi-chart-bell-curve-cumulative</v-icon>
          <span class="title">Multicollinearity Assessment</span>
        </v-card>
      </v-col>
      <v-col cols="6" class="mt-3">
        <v-card hover outlined rounded class="pa-3 text-center" @click="$router.push({name: 'FeatureSelector'})">
          <v-icon x-large>mdi-select-all</v-icon>
          <span class="title">Feature Selector</span>
        </v-card>
      </v-col>

    </v-row>
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
