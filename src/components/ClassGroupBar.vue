<template>
  <div>
    <div >
      Use the slider to adjust your training data class size.
    </div>
    <v-row>
      <v-col cols="5">
        <v-slider
          :min="minSampleSize"
          :max="maxSampleSize"
          v-model="trainingClassSize"
          @change="calculateGroupCounts"

        ></v-slider>
      </v-col>
      <v-col cols="1">
        {{trainingClassSize}}
      </v-col>
    </v-row>
    <div>
      <v-alert type="warning" text v-if="trainingClassSize < 50">
        We recommend a minimum training class size of 50.
        <span v-if="maxSampleSize < 50"> However, we also require a minimum generalization class size of 25.</span>
      </v-alert>

    </div>
    <div >
      Select how you would like to use remain data in the global generalization testing set.
    </div>
    <v-radio-group
      v-model="prevalenceOption"
      @change="calculateGroupCounts"
    >
      <v-radio label="Use All Remaining Data After Training Data Removed"></v-radio>
      <v-radio label="Maintain Original Prevalence in Validation File (some data may be excluded)"></v-radio>
    </v-radio-group>
    <div style="width:100%">
      <div>
        <div
          class="title-box"
          v-bind:style="{
            background: 'white',
            width: countToPercent(counts.nan, counts.total) + '%'
            }"
          >
        </div>


        <div
          class="title-box"
          v-bind:style="{
            background: '#7E57C2',
            width: countToPercent(counts.train1, counts.total) + countToPercent(counts.train0, counts.total)  + '%'
            }"
          >
          Training Data
        </div>
        <div
          class="title-box"
          v-bind:style="{
            background: '#5C6BC0',
            width: countToPercent(counts.test1, counts.total) + countToPercent(counts.test0, counts.total) + '%'
            }"
          >
          Generalization Testing Data
        </div>
      </div>
      <div style="width:100%">

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <div
            class="distrobution-box"
            v-bind="attrs"
            v-on="on"
            v-bind:style="{
              background: 'grey',
              width: countToPercent(counts.nan, counts.total) + '%'
              }"
            >
            <div>
              Miss Data
            </div>
            <div>n={{counts.nan}}</div>
          </div>

        </template>
        <span>{{counts.nan}} rows are missing data and cannot be used in the final data set</span>
      </v-tooltip>
      <div
        class="distrobution-box"
        v-bind:style="{
          background: '#64B5F6',
          width: countToPercent(counts.train0, counts.total) + '%'
          }"
        >
        <div>Train 0</div>
        <div>n={{counts.train0,}}</div>
      </div>
      <div
        class="distrobution-box"
        v-bind:style="{
          background: '#4DB6AC',
          width: countToPercent(counts.train1, counts.total) + '%'
          }"
        >
        <div>Train 1</div>
        <div>n={{counts.train1}}</div>
      </div>
      <div
        class="distrobution-box"
        v-bind:style="{
          background: '#42A5F5',
          width: countToPercent(counts.test0, counts.total) + '%'
          }"
        >
        <div>Test 0</div>
        <div>n={{counts.test0}}</div>
      </div>
      <div
        class="distrobution-box"
        v-bind:style="{
          background: '#26A69A',
          width: countToPercent(counts.test1, counts.total) + '%'
          }"
        >
        <div>Test 1</div>
        <div>n={{counts.test1}}</div>
      </div>
      <div
        class="distrobution-box"
        v-bind:style="{
          background: '#F48FB1',
          width: countToPercent(counts.extra, counts.total) + '%'
          }"
        >
        <div>Not Used</div>
        <div>n={{counts.extra}}</div>
      </div>
      </div>
    </div>
  </div>

</template>
<script>
export default {
  name: 'ClassGroupBar',
  props: ['metadata'],
  data() {
    return {
      // metadata: {
      //   class_counts: {
      //     0: 200,
      //     1: 309
      //   },
      //   majority_class: 1,
      //   minority_class: 0,
      //   nan_class_counts: {
      //     0: 8,
      //     1: 11
      //   },
      //   total_count: 509
      // },

      prevalenceOption: 0,


      minSampleSize: 25,
      maxSampleSize: 5000, //changed programatically
      trainingClassSize: 50,

      minBoxSize: 10, //sets smallest % for any group on the bar

      counts: {
        nan: 0,
        class0: 0,
        class1: 0,
        train0: 0,
        train1: 0,
        test0: 0,
        test1: 0,
        extra: 0,
        total: 1,
      },
      prevalence: {
        class0: 0,
        class1: 0
      },
    }
  },
  computed: {
    scaleFactorForMinBoxes() {
      let scaler = 100
      for (let item in this.counts) {
        if (item != 'total') {
          let num = this.counts[item]
          let val = 100 * (num / this.counts.total )
          if (val <= this.minBoxSize && val > 0) {
            scaler = scaler - (this.minBoxSize - val) - 3
          }


        }
      }
      return scaler / 100
    }
  },
  mounted() {
    this.calculateClassCounts()
    this.findTrainingClassSampleSize()
    this.calculateMaxSampleSize()
    this.calculateGroupCounts()


  },
  methods: {
    calculateClassCounts() {
      console.log(this.metadata)
      //Transfer metadata for total
      this.counts.total = this.metadata.total_count
      //Ajust counts based on missing data. API always returns 0 for each class if no rows are misisng ata.
      this.counts.nan = this.metadata.nan_class_counts[0] + this.metadata.nan_class_counts[1]
      this.counts.class0 = this.metadata.class_counts[0] - this.metadata.nan_class_counts[0]
      this.counts.class1 = this.metadata.class_counts[1] - this.metadata.nan_class_counts[1]
      //Post missing data prevalence
      this.prevalence.class0 = this.counts.class0 / (this.counts.total - this.counts.nan)
      this.prevalence.class1 = this.counts.class1 / (this.counts.total - this.counts.nan)
    },
    calculateGroupCounts() {
      //Training
      this.counts.train0 = this.trainingClassSize
      this.counts.train1 = this.trainingClassSize

      //Testing
      //Use all remaining data
      if (this.prevalenceOption == 0) {
        this.counts.test0 = this.counts.class0 - this.trainingClassSize
        this.counts.test1 = this.counts.class1 - this.trainingClassSize
        this.counts.extra = 0
      }
      else if (this.prevalenceOption == 1) {
        if (this.prevalence.class0 < 0.5) {

          this.counts.test0 = this.counts.class0 - this.trainingClassSize
          this.counts.test1 = Math.round((this.counts.test0 / this.prevalence.class0) - this.counts.test0)
          this.counts.extra = this.counts.total - this.counts.nan - this.counts.train0 - this.counts.train1 - this.counts.test0 - this.counts.test1

        }
        else if (this.prevalence.class1 < 0.5) {

          this.counts.test1 = this.counts.class1 - this.trainingClassSize
          this.counts.test0 = Math.round((this.counts.test1 / this.prevalence.class1) - this.counts.test1)
          this.counts.extra = this.counts.total - this.counts.nan - this.counts.train0 - this.counts.train1 - this.counts.test0 - this.counts.test1

        }
        else if (this.prevalence.class0 == 0.5) {
          this.counts.test0 = this.counts.class0 - this.trainingClassSize
          this.counts.test1 = this.counts.class1 - this.trainingClassSize
          this.counts.extra = 0
        }
      }
      //emit calculations to parent component
      this.reportData()
    },
    countToPercent(num, denom) {
      let val = 100 * (num / denom )
      if (num == 0) {
        return 0
      }
      else if (val <= this.minBoxSize) {
        return this.minBoxSize
      }
      else {
        return (val * this.scaleFactorForMinBoxes)
      }

    },
    findTrainingClassSampleSize() {
      let minortyCount = this.prevalence.class0 < 0.5 ? this.counts.class0 : this.counts.class1
      let halfMinorityCount = Math.round(minortyCount / 2)
      if (this.minSampleSize > halfMinorityCount) {
        this.trainingClassSize = this.minSampleSize
      }
      else {
        this.trainingClassSize = halfMinorityCount
      }

    },
    calculateMaxSampleSize() {
      let minortyCount = this.prevalence.class0 < 0.5 ? this.counts.class0 : this.counts.class1
      this.maxSampleSize = minortyCount - this.minSampleSize > 2500 ? 2500 : minortyCount - this.minSampleSize
    },
    reportData() {
      let calculation = {
        prevalenceOption: this.prevalenceOption,
        trainingClassSize: this.trainingClassSize,
        extraCount: this.counts.extra
      }
      this.$emit('calculation', calculation)
    }

  }

}
</script>
