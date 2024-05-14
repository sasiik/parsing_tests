const puppeteer = require("puppeteer");

async function fetchAndExtractVariable(url) {
	const browser = await puppeteer.launch();
	const page = await browser.newPage();

	await page.goto(url, { waitUntil: "networkidle2" });
	const nuxtData = await page.evaluate(() => {
		return window.__NUXT__;
	});

	const data = nuxtData.payload.state.payload["products"];
	const processed_data = data.map((product) => {
		return {
			name: product["name"] ? product["name"] : "No name",
			brand: product["brand"]["name"]
				? product["brand"]["name"]
				: "No brand",
			gender: product["gender"] ? product["gender"] : "No gender",
			price: product["price_amount"] + " " + product["price_iso_code"],
			type: product["type"] ? product["type"] : "No type",
			category_type: product["category_type"]
				? product["category_type"]
				: "No category type",
			brand_size_system: product["brand_size_system"]
				? product["brand_size_system"]
				: "No size system",
			color_family: product["color_family"]
				? product["color_family"]
				: "No color family",
		};
	});

	await browser.close();
	console.log(processed_data);
	return processed_data;
}

const Excel = require("exceljs");

async function createProductWorksheet(products) {
	const workbook = new Excel.Workbook();
	const worksheet = workbook.addWorksheet("Products");

	worksheet.columns = [
		{ header: "Name", key: "name", width: 30 },
		{ header: "Brand", key: "brand", width: 25 },
		{ header: "Gender", key: "gender", width: 15 },
		{ header: "Price", key: "price", width: 20 },
		{ header: "Type", key: "type", width: 20 },
		{ header: "Category Type", key: "category_type", width: 20 },
		{ header: "Brand Size System", key: "brand_size_system", width: 20 },
		{ header: "Color Family", key: "color_family", width: 20 },
	];

	products.forEach((product) => {
		worksheet.addRow({
			name: product.name,
			brand: product.brand,
			gender: product.gender,
			price: product.price,
			type: product.type,
			category_type: product.category_type,
			brand_size_system: product.brand_size_system,
			color_family: product.color_family,
		});
	});

	try {
		await workbook.xlsx.writeFile("lamoda/output/output.xlsx");
		console.log('Excel file "output.xlsx" has been created successfully.');
	} catch (err) {
		console.error("Error writing to Excel file:", err);
	}
}
const base_url = "https://www.lamoda.ru/c/4153/default-women/";
var data_vault = [];

async function fetchAllPages() {
	for (let i = 1; i <= 5; i++) {
		try {
			const processed_data = await fetchAndExtractVariable(
				base_url + `?page=${i}`
			);
			data_vault.push(...processed_data);
			console.log(`Processed page ${i}`);
		} catch (error) {
			console.error(`Failed to fetch or process page ${i}:`, error);
		}
	}
	console.log(data_vault);
	createProductWorksheet(data_vault);
	console.log("All data has been processed and worksheet created.");
}

fetchAllPages();
