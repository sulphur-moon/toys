<template>
	<view class="content">
		<view class="heroCategary">
			<view class="title">
				力量英雄
			</view>
			<view class="heroSelect red">
				<image v-for="index in index_strength" :src="pre_fix + array[index].pic_url" :key="index" class="item" mode="aspectFit" @click="select(index)"></image>
			</view>
			<view class="title">
				敏捷英雄
			</view>
			<view class="heroSelect green">
				<image v-for="index in index_agility" :src="pre_fix + array[index].pic_url" :key="index" class="item" mode="aspectFit" @click="select(index)"></image>
			</view>
			<view class="title">
				智力英雄
			</view>
			<view class="heroSelect blue">
				<image v-for="index in index_intelligence" :src="pre_fix + array[index].pic_url" :key="index" class="item" mode="aspectFit" @click="select(index)"></image>
			</view>
		</view>
		
	</view>
</template>

<script>
	import {strength, agility, intelligence} from './hero_category.js'
	import {hero_dict} from './json_hero.js';
	export default {
		data() {
			return {
				array: hero_dict,
				index_strength: strength,
				index_agility: agility,
				index_intelligence: intelligence,
				pre_fix: '../../static/hero_pic/'
			}
		},
		onLoad() {
			/*console.log(typeof(this.array));
			let keys = Object.keys(this.array)
			console.log(keys)
			for(let a of this.index_agility) {
				console.log(a, keys.indexOf(a));
			}
			for(let i of this.index_intelligence) {
				console.log(i, keys.indexOf(i));
			}*/
		},
		methods: {
			select: function(e) {
				console.log(e)
				let pages = getCurrentPages();
				let nowPage = pages[pages.length - 1];
				let prevPage = pages[pages.length - 2];
				console.log(prevPage.$vm.flg);
				if (prevPage.$vm.flg) {
					console.log(prevPage.$vm.anti_now);
					this.$set(prevPage.$vm.anti_index, prevPage.$vm.anti_now, e);
				} else {
					console.log(prevPage.$vm.comb_now);
					this.$set(prevPage.$vm.comb_index, prevPage.$vm.comb_now, e);
				}
				uni.navigateBack({
					delta:1
				})
			}
		}
	}
</script>

<style>
	.heroCategary {
		display: flex;
		flex-direction: column;
		flex-wrap: nowrap;
	}
	
	.heroSelect {
		padding-left: 25upx;
		padding-top: 10upx;
		padding-bottom: 10upx;
		padding-right: 25upx;
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: flex-start;
	}
	
	.green {
		background-color: rgba(0, 255, 0, 0.8);
	}
	
	.blue {
		background-color: rgba(0, 0, 255, 0.8);
	}
	
	.red {
		background-color: rgba(255, 0, 0, 0.8);;
	}
	
	.title {
		padding-top: 20upx;
		text-align: center;
	}
	.item {
		width: 140upx;
		height: 80upx;
	}
	.gray {
		filter: grayscale();
	}
</style>
