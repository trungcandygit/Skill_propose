# PROMPT: Viết đề cương "KH, CN, ĐMST và CĐS đóng góp vào GRDP tỉnh Quảng Ninh"

> Cách dùng: mở một phiên Claude Code mới, dán toàn bộ phần dưới đường kẻ.

---

## 0. Thiết lập (làm trước mọi việc khác)

1. Clone repo skill: `git clone --depth 1 https://github.com/trungcandygit/Skill_propose`. Chép thư mục `research-proposal-master/` vào `.claude/skills/` của thư mục làm việc (hoặc `~/.claude/skills/`).
2. Kiểm tra Skill tool nhận skill `research-proposal-master`, rồi gọi `Skill("research-proposal-master")`.
3. Đọc trọn vẹn, không đọc theo đoạn:
   - `SKILL.md`
   - `references/cards/core.md`
   - `references/cards/proposal.md`
   - `references/cards/deep-search.md`
   - `references/cards/orchestrator.md`
4. Ghi dòng `Loaded:` gồm tên file, số dòng và sentinel `CARD-END` của từng file. Thiếu dòng này thì coi như chưa làm.
5. Làm đúng spine P0 → P8 của skill:
   - Dừng ở các điểm kiểm tra: duyệt outline (P-90), duyệt bảng mục tiêu và giả thuyết.
   - Panel 2 agent, tối đa 2 agent chạy cùng lúc. Lặp đến khi không còn CRITICAL và MAJOR.
   - Mọi phát hiện phải ghi mã luật (C-xx, P-xx, DS-xx).
6. Chỉ làm việc trên repo hoặc thư mục tôi chỉ định. Không đụng repo khác. Không fork, không tạo PR. Repo skill chỉ được đọc, trừ khi tôi bảo cập nhật skill (khi đó theo `maintain.md`).

## 1. Đề tài

**Tên đề tài (giữ nguyên, không tự đổi):**
> Nghiên cứu đóng góp của khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số vào tăng trưởng kinh tế (GRDP) tỉnh Quảng Ninh giai đoạn 2021–2025 và giải pháp thúc đẩy đến năm 2030, tầm nhìn 2050

**Việc đầu tiên ở P0 là hỏi tôi** (không tự đoán):
- Loại hồ sơ: đề tài KH&CN cấp tỉnh (thuyết minh theo mẫu của Bộ KH&CN hoặc Sở KH&CN Quảng Ninh), đề cương luận án hay luận văn, hay đề án tư vấn chính sách.
- Mẫu, biểu mẫu, giới hạn trang, thời gian thực hiện, kinh phí, cơ quan chủ trì.
- Tôi đã có những tài liệu và dữ liệu nào.

Chưa có mẫu thì dùng cấu trúc P-60, nhưng ghi rõ là tạm.

## 2. Căn cứ lý thuyết: phải đi theo đúng trình tự này

Phần lý thuyết **bắt đầu từ việc GRDP là gì**, rồi mới đến chuyện **bốn yếu tố đóng góp vào GRDP như thế nào**. Không viết chung chung kiểu "KH-CN là động lực then chốt". Mỗi khái niệm phải có định nghĩa chính thức, nguồn gốc và cách đo.

### 2.1 Tăng trưởng kinh tế và GRDP

- **Định nghĩa.**
  - GRDP (tổng sản phẩm trên địa bàn) theo văn bản chính thức hiện hành của Việt Nam: hệ thống chỉ tiêu thống kê quốc gia và cấp tỉnh, phương pháp biên soạn GRDP thống nhất giữa trung ương và địa phương.
  - Deep search tới văn bản gốc, ghi số hiệu, ngày, điều, khoản và trích nguyên văn. Không tự nhớ số hiệu văn bản; chưa xác minh được thì ghi [CẦN XÁC MINH].
  - Phân biệt GRDP với GDP và GNI.
- **Cách tính GRDP.** Ba phương pháp: sản xuất, sử dụng, thu nhập. Phân biệt giá hiện hành và giá so sánh (năm gốc 2010), cơ cấu ngành, thuế sản phẩm trừ trợ cấp. Ghi rõ GRDP bình quân đầu người và GRDP theo giá so sánh được dùng để đo tăng trưởng.
- **Tăng trưởng kinh tế.**
  - Định nghĩa: tốc độ tăng GRDP thực theo giá so sánh.
  - Phân biệt tăng trưởng theo chiều rộng (tăng vốn K, lao động L) và theo chiều sâu (năng suất, TFP).
  - Chất lượng tăng trưởng.
  - Chỉ tiêu "tỷ trọng đóng góp của TFP vào tăng trưởng": định nghĩa và cách Tổng cục Thống kê / Cục Thống kê tính. Xác minh văn bản quy định phương pháp.
- **Lý thuyết tăng trưởng** (đọc bài gốc, ghi tạp chí, tập, số, trang, DOI):
  - Harrod-Domar.
  - Solow (1956), Swan (1956).
  - Solow (1957), hạch toán tăng trưởng và phần dư TFP.
  - Tăng trưởng nội sinh: Romer (1986, 1990); Lucas (1988); Aghion & Howitt (1992); Grossman & Helpman (1991).
  - Jones (1995) về hiệu ứng quy mô.
  - Hạch toán tăng trưởng theo Jorgenson. Tách vốn ICT và vốn phi ICT: Jorgenson & Stiroh (2000), Oliner & Sichel (2000).
- **Khung phân tích cấp vùng và tỉnh:** tăng trưởng vùng, hội tụ (Barro & Sala-i-Martin), lan tỏa không gian, lợi thế tích tụ.

### 2.2 Bốn yếu tố và kênh đóng góp vào GRDP

Mỗi yếu tố phải viết đủ bốn ý: (a) khái niệm chính thức, (b) cách đo và chỉ báo cấp tỉnh có dữ liệu thật, (c) kênh tác động lên GRDP và cơ sở lý thuyết, (d) bằng chứng thực nghiệm. Mỗi bằng chứng phải ghi mẫu, giai đoạn, phương pháp, hệ số và số bảng.

1. **Khoa học (nghiên cứu khoa học, R&D).**
   - Khái niệm theo Luật Khoa học và Công nghệ hiện hành (xác minh bản mới nhất và điều khoản định nghĩa) và theo Frascati Manual (OECD, 2015).
   - Kênh tác động: tích lũy tri thức, hàm sản xuất tri thức (Griliches, 1979), vốn R&D, lan tỏa tri thức.
   - Bằng chứng: Coe & Helpman (1995); các bài về Việt Nam và cấp tỉnh.
   - Chỉ báo: chi R&D/GRDP, số cán bộ nghiên cứu, công bố, sáng chế, đề tài.
2. **Công nghệ.**
   - Khái niệm theo Luật Chuyển giao công nghệ và Luật KH&CN.
   - Kênh tác động: đổi mới thiết bị, chuyển giao và hấp thụ công nghệ, khả năng hấp thụ (Cohen & Levinthal, 1990), FDI và lan tỏa công nghệ, trình độ công nghệ của doanh nghiệp.
   - Chỉ báo: đầu tư máy móc thiết bị, tỷ trọng ngành công nghệ cao, hợp đồng chuyển giao công nghệ, FDI công nghệ.
3. **Đổi mới sáng tạo.**
   - Khái niệm theo Oslo Manual (OECD/Eurostat, 2018) và văn bản Việt Nam.
   - Kênh tác động: Schumpeter, phá hủy sáng tạo, hệ thống đổi mới sáng tạo quốc gia và vùng (Freeman; Lundvall; Cooke), hệ sinh thái khởi nghiệp.
   - Chỉ báo: Chỉ số đổi mới sáng tạo cấp địa phương (PII) của Bộ KH&CN (xác minh năm bắt đầu, phương pháp, điểm và hạng của Quảng Ninh), doanh nghiệp KH&CN, startup.
4. **Chuyển đổi số.**
   - Khái niệm theo văn bản Việt Nam (Chương trình chuyển đổi số quốc gia; xác minh số hiệu) và OECD.
   - Kênh tác động: vốn ICT, kinh tế số, chính quyền số giảm chi phí giao dịch, nền tảng số (Brynjolfsson & Hitt, 2000; Brynjolfsson, Rock & Syverson về "productivity J-curve").
   - Chỉ báo: Chỉ số chuyển đổi số cấp tỉnh (DTI), tỷ trọng kinh tế số trong GRDP (xác minh phương pháp đo chính thức), hạ tầng số.

**Bắt buộc:**
- Vẽ khung khái niệm: bốn yếu tố → kênh trung gian (TFP, năng suất lao động, vốn ICT, chuyển dịch cơ cấu, chất lượng thể chế) → GRDP.
- Mỗi mũi tên phải có lập luận và nguồn đi kèm (P-15).
- Nêu rõ bốn yếu tố **chồng lấn** nhau (ví dụ CĐS là một dạng ĐMST, R&D là đầu vào của công nghệ) và cách đề tài tách chúng ra. Không cộng trùng phần đóng góp.

### 2.3 Căn cứ chính sách (deep search văn bản gốc)

- **Văn bản cần tìm và xác minh**, mỗi văn bản ghi số hiệu, ngày, điều, khoản, chỉ tiêu và trích nguyên văn:
  - Nghị quyết của Bộ Chính trị về đột phá phát triển KH, CN, ĐMST và CĐS quốc gia (Nghị quyết 57-NQ/TW, xác minh ngày ban hành);
  - nghị quyết của Chính phủ triển khai nghị quyết đó;
  - Luật KH&CN và luật về ĐMST mới nhất nếu có;
  - Chiến lược KH, CN và ĐMST đến 2030;
  - Chương trình chuyển đổi số quốc gia;
  - Quy hoạch tỉnh Quảng Ninh thời kỳ 2021–2030, tầm nhìn 2050;
  - Nghị quyết Đại hội Đảng bộ tỉnh nhiệm kỳ 2020–2025 và 2025–2030;
  - nghị quyết hoặc kế hoạch của tỉnh về KH-CN, ĐMST và CĐS;
  - chỉ tiêu tỷ trọng đóng góp TFP và tỷ trọng kinh tế số trong các văn bản trên.
- Xác minh việc **sắp xếp đơn vị hành chính năm 2025** có làm thay đổi ranh giới, số liệu hay chuỗi thời gian của Quảng Ninh không.

## 3. Thiết kế nghiên cứu: phải nói thật về giới hạn nhận dạng

- **Chuỗi 2021–2025 của một tỉnh chỉ có 5 điểm năm.** Không thể hồi quy chuỗi thời gian cho riêng Quảng Ninh rồi gọi đó là "tác động". Agent phải đề xuất và so sánh các phương án, kèm decision record (P-103), rồi để tôi chọn. Ví dụ:
  - **(a) Hạch toán tăng trưởng mở rộng cho Quảng Ninh:** tách đóng góp của K (vốn ICT và phi ICT), L (có điều chỉnh chất lượng) và TFP. Có thể mở rộng sang vốn R&D. Ghi rõ đây là phân rã kế toán, không phải nhân quả.
  - **(b) Hồi quy dữ liệu bảng các tỉnh trong giai đoạn dài hơn** (ví dụ 2011–2024, tùy dữ liệu), với các chỉ báo KH, CN, ĐMST và CĐS: ước lượng hệ số co giãn rồi áp vào Quảng Ninh. Cần xử lý nội sinh (độ trễ, IV nếu có, GMM với kiểm định Hansen/AR(2)) và lan tỏa không gian (mô hình không gian). Thận trọng khi diễn giải nhân quả (C-20 đến C-22).
  - **(c) So sánh Quảng Ninh với nhóm tỉnh đối chứng** (synthetic control, nếu có biến cố chính sách rõ ràng).
  - **(d) Phương pháp hỗn hợp** cho phần giải pháp 2030/2050: phỏng vấn chuyên gia, Delphi hoặc AHP, kịch bản dự báo. Phần này tách khỏi phần định lượng.
- **Với mỗi phương án**, ghi: ước lượng mục tiêu (estimand), giả định, mối đe dọa, dữ liệu cần có và trạng thái của dữ liệu, cùng MDE hoặc độ chính xác kỳ vọng (P-30 đến P-38).
- **Dữ liệu:**
  - Danh mục cần có: Niên giám thống kê Quảng Ninh; GRDP theo giá so sánh; vốn đầu tư; lao động; chi KH-CN; PII; DTI; PCI; điều tra doanh nghiệp; số liệu kinh tế số.
  - Mỗi biến ghi nguồn, phạm vi năm, có hay chưa, cách xin.
  - Biến nào không có dữ liệu thật thì không được đưa vào mô hình chính.

## 4. Câu hỏi, mục tiêu và sản phẩm

- **Đề xuất cho tôi duyệt:** 1 mục tiêu tổng quát, 3–4 mục tiêu cụ thể, câu hỏi nghiên cứu và giả thuyết có hướng tương ứng. Lập ma trận nhất quán (P-71).
- **Dùng từ đúng với thiết kế:** "đóng góp", "phân rã", "liên hệ" khác với "tác động". Không hứa nhân quả nếu thiết kế không cho phép (P-23).
- **Giải pháp 2030, tầm nhìn 2050:**
  - Phải bám vào kết quả phân tích và vào chỉ tiêu trong văn bản của tỉnh.
  - Ghi rõ cơ quan thực hiện và chỉ báo theo dõi.
  - Không đưa ra giải pháp chung chung có thể áp cho tỉnh nào cũng được.
- **Sản phẩm:** báo cáo tổng hợp; bộ chỉ số hoặc bộ dữ liệu; bài báo (nêu tạp chí dự kiến); kiến nghị chính sách. Mỗi sản phẩm gắn với một mục tiêu và một mốc thời gian.

## 5. Tìm kiếm sâu và tài liệu (thẻ deep-search)

- **Mỗi dữ kiện** (văn bản, số liệu GRDP, TFP, PII, DTI, chỉ tiêu quy hoạch) phải có đủ: nguồn gốc, vị trí trong nguồn, trích nguyên văn, URL, ngày truy cập, trạng thái KHỚP / LỆCH / CHƯA CÓ NGUỒN (DS-01).
- **Không dùng báo chí làm nguồn cuối cùng.** Không viết câu chung chung kiểu chiến lược.
- **Văn liệu:**
  - Tìm bản đã xuất bản (DOI) và đọc bảng kết quả.
  - Ưu tiên các nghiên cứu về TFP và tăng trưởng cấp tỉnh ở Việt Nam, bằng chứng về ICT, R&D và ĐMST ở cấp vùng (Trung Quốc, EU NUTS-2), cùng các bài kinh điển ở mục 2.
  - Ghi nhật ký tìm kiếm (DS-42).
- **Tài liệu bạn không mở được:** dừng lại và **nhắn tôi danh sách SIÊU ĐẦY ĐỦ** để tôi tự tìm và tải (P-06, DS-43).
  - Mỗi tài liệu ghi: tên chính xác; cơ quan hoặc tác giả; năm; số hiệu hoặc DOI; vì sao cần; dùng ở mục nào; cần phần nào; tìm ở đâu; từ khoá tiếng Việt và tiếng Anh; định dạng mong muốn; mức ưu tiên.
  - Gộp danh sách theo nhóm: văn bản trung ương; văn bản của tỉnh; số liệu thống kê; chỉ số (PII, DTI, PCI); văn liệu quốc tế; văn liệu Việt Nam.
  - Nhắc lại danh sách ở đầu mỗi vòng cho đến khi tôi gửi đủ.

## 6. Quy tắc trình bày

- **Ngôn ngữ:** tiếng Việt học thuật. Câu có chủ ngữ rõ. Không dùng các cụm sáo rỗng như "trong bối cảnh hiện nay", "đóng vai trò then chốt", "ngày càng thu hút sự quan tâm" (P-102). Viết thành đoạn văn, không gạch đầu dòng tràn lan (P-93).
- **Trích dẫn APA 7:** trong ngoặc dùng "&", ví dụ (Coe & Helpman, 1995); ngoài ngoặc dùng "và", ví dụ Coe và Helpman (1995). Trích dẫn và danh mục tài liệu phải khớp hai chiều. Văn bản pháp lý trích đủ số hiệu, loại văn bản, cơ quan ban hành, ngày.
- **Không bịa:** không bịa trích dẫn, số liệu hay số hiệu văn bản. Chưa xác minh được thì ghi [CẦN XÁC MINH].
- **Sản phẩm mỗi vòng:**
  - một file .docx sạch, không track changes;
  - nhật ký thay đổi;
  - danh sách [CẦN XÁC MINH] còn lại;
  - danh sách tài liệu cần tôi tìm.

  Lưu theo `outputs/round-N/`.
- **Trước khi push** file đề cương hoặc tài liệu: kiểm tra repo có phải private không. Nếu repo public, hỏi tôi trước (P-66).

## 7. Việc làm ngay trong phiên đầu

1. Thiết lập (mục 0) và ghi `Loaded:`.
2. Hỏi tôi các câu ở mục 1 về loại hồ sơ và mẫu. Nếu cần, chạy phỏng vấn spec (P-92) theo `skills/interview-me`, mỗi lượt 1–2 câu hỏi.
3. Gửi tôi danh sách tài liệu và dữ liệu cần tìm (bản đầu tiên, đầy đủ nhất có thể).
4. Đề xuất outline, khung lý thuyết (mục 2) và 2–3 phương án thiết kế (mục 3) kèm decision record. **Dừng lại chờ tôi duyệt** (P-90). Chưa viết toàn văn.

**Nhắc lại: làm ĐẦY ĐỦ, CỤ THỂ, CHÍNH XÁC.** Kết luận nào cũng phải có nguồn. Thiếu tài liệu thì nhắn tôi kèm danh sách chi tiết. Không bỏ bước để tiết kiệm (C-60 đến C-62).
