#include <algorithm>
#include <random>
#include <sstream>

#include <twg/twg.h>
#include <twg/image.h>
#include <twg/image/image_drawing.h>

typedef const std::wstring& wstr;

double random(void) {
	static std::mt19937 generator(1);
	static std::uniform_real_distribution<double> distribution(0, 1);
	return distribution(generator);
}

int random(int start, int end) {
	return random() * (end - start) + start;
}

using namespace twg;

#undef min
#undef max

void cut_background(wstr name, int count, double size) {
	static int counter = 1;
	ImageBase img(Point_i(1, 1));
	loadFromPngJpg(&img, name);

	int n = std::min(img.width(), img.height()) * size;

	for (int i = 0; i < count; i++) {
		int posx = random(0, img.width() - n);
		int posy = random(0, img.height() - n);
		Point_i pos(posx, posy);

		ImageBase img2(Point_i(n, n));
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				Point_i current(x, y);
				img2[current] = img[pos + current];
			}
		}
		std::wstringstream sout;
		sout << "processed_backgrounds/" << counter << ".png";
		counter++;
		saveToPng(&img2, sout.str());
	}
}

void merge_background_and_image(wstr image, wstr mask, wstr background, wstr result) {
	ImageBase img(Point_i(1, 1)); loadFromPngJpg(&img, image);
	ImageBase imgm(Point_i(1, 1)); loadFromPngJpg(&imgm, mask);
	ImageBase imgb(Point_i(1, 1)); loadFromPngJpg(&imgb, background);
	ImageBase imgr(img.size());

	imgb.drawTo(&imgr, Point_i(0, 0), Point_i(0, 0), imgb.size(), imgr.size());
	for (int x = 0; x < imgr.width(); x++) {
		for (int y = 0; y < imgr.height(); y++) {
			Point_i current(x, y);
			if (imgm[current] != Red)
				imgr[current] = img[current];
		}
	}
	saveToPng(&imgr, result);
}

int counter1 = 1;
void merge_all_backgrounds_and_image(wstr image, wstr mask, int count, wstr back_path, wstr result_path) {
	for (int i = 1; i <= count; i++) {
		std::wstringstream sout;
		sout << back_path << i << ".png";

		std::wstringstream sout2;
		sout2 << result_path << counter1 << ".png";
		counter1++;
		merge_background_and_image(image, mask, sout.str(), sout2.str());
	}
}

int main() {
	int backMake = 2;
	double backSize = 0.75;
	int backCount = 10;
	int catCount = 23;
	int dogCount = 23;

	system("mkdir processed_backgrounds");
	for (int i = 1; i <= backCount; i++) {
		std::wstringstream sout;
		sout << "backgrounds/" << i << ".jpg";
		cut_background(sout.str(), backMake, backSize);
	}

	system("mkdir processed_cats");
	counter1 = 1;
	for (int i = 1; i <= catCount; i++) {
		std::wstringstream sout;
		sout << "cats/" << i << ".jpg";

		std::wstringstream sout2;
		sout2 << "cats_mask/" << i << ".png";
		merge_all_backgrounds_and_image(sout.str(), sout2.str(), backCount * backMake, L"processed_backgrounds/", L"processed_cats/");
	}

	system("mkdir processed_dogs");
	counter1 = 1;
	for (int i = 1; i <= dogCount; i++) {
		std::wstringstream sout;
		sout << "dogs/" << i << ".jpg";

		std::wstringstream sout2;
		sout2 << "dogs_mask/" << i << ".png";
		merge_all_backgrounds_and_image(sout.str(), sout2.str(), backCount * backMake, L"processed_backgrounds/", L"processed_dogs/");
	}
}