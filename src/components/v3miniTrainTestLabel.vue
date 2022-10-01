<template>
    <div class="inline-div">
        <v-chip small v-if="type == 'train'" color="purple" dark>Training</v-chip>
        <v-chip small v-if="type == 'test'" color="pink" dark>Testing</v-chip>
        <v-chip small v-if="type == 'combined'" color="orange" dark>Combined</v-chip>
    </div>
</template>
<script>    
export default {
    name: 'v3miniValidate',
    props: {
        type: {
            type: String,
            default: 'combined'
        },
    }
}
</script>
<style scoped>
.inline-div {
    display: inline;
}
</style>