<template>
	<view class="content">
		<view class="heroSelect">
			<view>对手英雄</view>
			<view class="heroSideSelect">
				<image v-for="index in anti_id" :src="array[anti_index[index]].pic_url" :key="index" class="item" mode="aspectFit" @click="antiBindPickerChange(index)"></image>
			</view>
			<view>队友英雄</view>
			<view class="heroSideSelect">
				<image v-for="index in comb_id" :src="array[comb_index[index]].pic_url" :key="index" class="item" mode="aspectFit" @click="combBindPickerChange(index)"></image>
				<image :src="btnUrl" class="item" mode="aspectFit" @click="calculate"></image>
			</view>
		</view>
		<view class="">
			<view>计算结果</view>
			<text style="text-align: left;font-size: 30upx;">{{result}}</text>
		</view>
	</view>
</template>

<script>
	import {hero_dict} from './json_hero.js';
	import {anti_dict} from './json_anti.js';
	import {comb_dict} from './json_comb.js';
	import {myLib} from './lib.js';
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
				cal: true,
				anti_id:[0, 1, 2, 3, 4],
				comb_id:[0, 1, 2, 3],
				btnUrl: "../../static/btn/calc.png",
				result: "",
				ans: []
			}
		},
		onLoad() {
			uni.showModal({
				title: "提示",
				content: "已选英雄不少于2个时，计算结果有效。第一次进入英雄选择页面时，图片载入需要一定时间，请耐心等待。",
				showCancel: false
			})
		},
		methods: {
			antiBindPickerChange: function(e) {
				//console.log("anti index:" + e);
				this.anti_now = e;
				this.flg = true;
				uni.navigateTo({
					url:'picker'
				})
			},
			combBindPickerChange: function(e) {
				//console.log("comb index:" + e)
				this.comb_now = e;
				this.flg = false;
				uni.navigateTo({
					url:'picker'
				})
			},
			calculate: function() {
				//console.log("calc");
				//console.log(this.anti_index);
				//console.log(this.comb_index);
				if (this.cal) {
					this.ans = [];
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
						for (let anti_hero of this.anti_index) {
							if (anti_hero == "选择英雄") {
								continue;
							}
							res.anti_rate.push(this.anti_dict[anti_hero][hero]['anti_rate']);
							res.anti_win_rate.push(this.anti_dict[anti_hero][hero]['win_rate']);
						}
						for (let comb_hero of this.comb_index) {
							if (comb_hero == "选择英雄") {
								continue;
							}
							res.comb_rate.push(this.comb_dict[comb_hero][hero]['comb_rate']);
							res.comb_win_rate.push(this.comb_dict[comb_hero][hero]['win_rate']);
						}
						let win_rates = res.anti_win_rate.concat(res.comb_win_rate);
						let rates = res.anti_rate.concat(res.comb_rate);
						let rate_sum = myLib.round2digit(myLib.sum(rates));
						let win_rate_mean = myLib.round2digit(myLib.mean(win_rates));
						let rate_std = myLib.round2digit(myLib.std(rates));
						res.eva = myLib.round2digit(win_rate_mean + rate_sum/rate_std);
						res.tot = win_rate_mean.toString() + ' + ' + rate_sum.toString() + '/' + rate_std.toString() + ' = ' + res.eva.toString();
						//console.log(rates, typeof(rates));
						//console.log("std = ", myLib.round2digit(myLib.std(rates)));
						this.ans.push(res);
					}
					this.ans.sort(function(a, b){
						return b.eva - a.eva;
					})
					//console.log(this.ans);
					//console.log(this.ans.length);
					this.result = "";
					for (let i = 0; i < 30; i++) {
						let a = this.ans[i];
						this.result += a.hero + "\n"
						if (a.anti_rate.length > 0) {
							this.result += a.anti_rate.join(' ') + '\n';
						}
						if (a.comb_rate.length > 0) {
							this.result += a.comb_rate.join(' ') + '\n';
						} 
						this.result += a.tot + "\n";
					}
					this.cal = false;
					this.btnUrl = "../../static/btn/clear.png";
				} else {
					for (let i = 0; i < this.anti_index.length; i++) {
						this.$set(this.anti_index, i, "选择英雄");
					}
					for (let i = 0; i < this.comb_index.length; i++) {
						this.$set(this.comb_index, i, "选择英雄");
					}
					this.cal = true;
					this.btnUrl = "../../static/btn/calc.png";
					this.result = "";
				}
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
