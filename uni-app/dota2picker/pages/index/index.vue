<template>
	<view class="content">
		<view class="heroSelect">
			<view>对手英雄</view>
			<view class="heroSideSelect">
				<image v-for="index in anti_id" :src="pre_fix + array[anti_index[index]].pic_url" :key="index" class="item" mode="aspectFit" @click="antiBindPickerChange(index)"></image>
			</view>
			<view>队友英雄</view>
			<view class="heroSideSelect">
				<image v-for="index in comb_id" :src="pre_fix + array[comb_index[index]].pic_url" :key="index" class="item" mode="aspectFit" @click="combBindPickerChange(index)"></image>
				<image src="../../static/hero_pic/calc.png" class="item" mode="aspectFit" @click="calculate"></image>
			</view>
		</view>
		<view class="">
			
		</view>
	</view>
</template>

<script>
	import {hero_dict} from './json_hero.js';
	import {anti_dict} from './json_anti.js';
	import {comb_dict} from './json_comb.js';
	export default {
		data() {
			return {
				array: hero_dict,
				anti_dict: anti_dict,
				comb_dict: comb_dict,
				anti_index: ["选择英雄", "选择英雄", "选择英雄", "选择英雄", "选择英雄"],
				comb_index: ["选择英雄", "选择英雄", "选择英雄", "选择英雄"],
				anti_now: 0,
				comb_now: 0,
				flg: true,
				anti_id:[0, 1, 2, 3, 4],
				comb_id:[0, 1, 2, 3],
				pre_fix: '../../static/hero_pic/'
			}
		},
		onLoad() {
			
		},
		methods: {
			antiBindPickerChange: function(e) {
				console.log("anti index:" + e);
				this.anti_now = e;
				this.flg = true;
				uni.navigateTo({
					url:'picker'
				})
			},
			combBindPickerChange: function(e) {
				console.log("comb index:" + e)
				this.comb_now = e;
				this.flg = false;
				uni.navigateTo({
					url:'picker'
				})
			},
			calculate: function() {
				console.log("calc");
				console.log(this.anti_index);
				console.log(this.comb_index);
				
				let ans = [];
				for (let hero in this.array) {
					if (hero == "选择英雄") {
						continue;
					}
					if (this.anti_index.indexOf(hero) != -1) {
						continue;
					}
					if (this.comb_index.indexOf(hero) != -1) {
						continue;
					}
					let res = {};
					res.hero = hero;
					res.anti_rate = [];
					res.anti_win_rate = [];
					res.comb_rate = [];
					res.comb_win_rate = [];
					res.tot = "";
					res.eva = 0;
					let win_rate = 0;
					for (let anti_hero of this.anti_index) {
						res.anti_rate.push(this.anti_dict[anti_hero][hero]['anti_rate']);
						res.anti_win_rate.push(this.anti_dict[anti_hero][hero]['win_rate']);
						win_rate += this.anti_dict[anti_hero][hero]['win_rate'];
					}
					for (let comb_hero of this.comb_index) {
						res.comb_rate.push(this.comb_dict[comb_hero][hero]['comb_rate']);
						res.comb_win_rate.push(this.comb_dict[comb_hero][hero]['win_rate']);
						win_rate += this.comb_dict[comb_hero][hero]['win_rate'];
					}
					res.eva = win_rate / (res.anti_win_rate.length + res.comb_win_rate.length);
					ans.push(res);
					let rates = res.anti_rate.concat(res.comb_rate);
					console.log(rates, typeof(rates));
				}
				console.log(ans);
				console.log(ans.length);
			}
		}
	}
</script>

<style>
	.content {
		text-align: center;
		height: 400upx;
	}

	.logo {
		height: 200upx;
		width: 200upx;
		margin-top: 200upx;
	}

	.title {
		font-size: 36upx;
		color: #8f8f94;
	}
	
	.heroSelect {
		display: flex;
		flex-direction: column;
		flex-wrap: nowrap;
	}
	
	.heroSideSelect {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
	}
	
	.green {
		background-color: green;
	}
	
	.blue {
		background-color: blue;
	}
	
	.red {
		background-color: red;
	}
	
	.black {
		background-color: black;
	}
	
	.orange {
		background-color: orange;
	}
	
	.item {
		width: 140upx;
		height: 80upx;
	}
</style>
