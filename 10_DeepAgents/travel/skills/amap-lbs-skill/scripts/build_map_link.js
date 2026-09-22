#!/usr/bin/env node

/**
 * 直接读取 MapTaskData 文件并生成高德个人地图（路线地图）可视化链接。
 * 用法: node scripts/build_map_link.js /path/to/taskdata.json
 */

const fs = require('fs');
const path = require('path');
const { generateMapLink } = require(path.join(__dirname, '..', 'index.js'));

const file = process.argv[2];
if (!file) {
  console.error('❌ 请提供 MapTaskData JSON 文件路径');
  process.exit(1);
}

const raw = fs.readFileSync(file, 'utf8');
const mapTaskData = JSON.parse(raw);

const mapLink = generateMapLink(mapTaskData);
const poiCount = mapTaskData.filter(i => i.type === 'poi').length;
const routeCount = mapTaskData.filter(i => i.type === 'route').length;

console.log('POI 数量:', poiCount);
console.log('路线数量:', routeCount);
console.log('MAP_LINK:');
console.log(mapLink);
