class Lib {
	constructor(arg) {
		
	}
	//数组求和
	sum(arr) {
		let res = 0;
		for (let a of arr) {
			res += a;
		}
		return res;
	}
	//数组平均值
	mean(arr) {
		let s = this.sum(arr);
		return s / arr.length;
	}
	//数组方差
	dvar(arr) {
		let m = this.mean(arr);
		let s = 0;
		for (let a of arr) {
			s += Math.pow(m - a, 2);
		}
		return s / (arr.length - 1);
	}
	//数组标准差
	std(arr) {
		return Math.sqrt(this.dvar(arr));
	}
	//保留两位小数
	round2digit(f) {
		return Math.round(f * 100) / 100;
	}
}

const myLib = new Lib();
export {myLib};