/* Network Tokenization: shared dummy values and the mapping rules of the PGW dev stories v1.1.
   All identifiers are dummy values (public site). The same dummy value is used on every NT page. */
(function () {
  var D = {
    mid: { mpgs: 'TEST-MPGS-01', cybs: 'TEST-CYBS-01' },
    brand: {
      visa: { scheme: 'VISA', name: 'Visa', provider: 'VTS', ps: '015', card: '411111xxxxxx1111', exp: { m: '02', y: '2029' },
              dsn: '489537xxxxxx0001', dsnExp: { month: '11', year: '28' }, tokenBin: '489537',
              par: 'V0010000000000000000000000001', ii: '7000000000000000001',
              tokenId: '0a1b2c3d-4e5f-6071-8293-a4b5c6d7e8f9' },
      mc: { scheme: 'MASTERCARD', name: 'Mastercard', provider: 'MDES', ps: '014', card: '512345xxxxxx0008', exp: { m: '09', y: '2030' },
            dsn: '522222xxxxxx0002', dsnExp: { month: '09', year: '29' }, tokenBin: '522222',
            par: '5001TESTPAR000000000000000002', ii: '7000000000000000002',
            tokenId: '1b2c3d4e-5f60-7182-93a4-b5c6d7e8f9a0' }
    },
    ntid: 'TESTNTID00001'
  };
  /* MPGS token = Geidea tokenId without dashes, upper case (merchant-supplied token). */
  D.mpgsToken = function (b) { return D.brand[b].tokenId.replace(/-/g, '').toUpperCase(); };

  /* NT-M2 to NT-M5 section "Mapping to networkTokenDetails". resp = MPGS transaction response (object). */
  D.mapMpgs = function (resp) {
    var sof = resp && resp.sourceOfFunds;
    if (!sof) return null;
    var c = (sof.provided && sof.provided.card) || {};
    var isNt = sof.type === 'SCHEME_TOKEN';
    var exp = c.deviceSpecificExpiry || {};
    return {
      isNetworkToken: isNt,
      tokenProvider: isNt ? ({ VISA: 'VTS', MASTERCARD: 'MDES' }[c.brand] || null) : null,
      maskedTokenNumber: c.deviceSpecificNumber || null,
      tokenExpiryMonth: exp.month || null,
      tokenExpiryYear: exp.year || null,
      paymentAccountReference: c.paymentAccountReference || null
    };
  };
  /* NT-C2 to NT-C4 section "Mapping to networkTokenDetails". resp = CYBS /pts/v2/payments response. */
  D.mapCybs = function (resp) {
    var ps = resp && resp.processingInformation && resp.processingInformation.paymentSolution;
    var isNt = ps === '015' || ps === '014';
    var bin = resp && resp.paymentInformation && resp.paymentInformation.card && resp.paymentInformation.card.bin;
    var par = resp && resp.processorInformation && resp.processorInformation.paymentAccountReferenceNumber;
    return {
      isNetworkToken: isNt,
      tokenProvider: ps === '015' ? 'VTS' : ps === '014' ? 'MDES' : null,
      maskedTokenNumber: isNt && bin ? bin + '0000000000' : null,
      tokenExpiryMonth: null,
      tokenExpiryYear: null,
      paymentAccountReference: par || null
    };
  };

  /* Illustrative gateway responses (excerpts). Field names are the stories' (MPGS v80, CYBS REST). */
  D.mpgsResp = function (b, nt, op) {
    var x = D.brand[b];
    var card = { brand: x.scheme };
    if (nt) { card.deviceSpecificNumber = x.dsn; card.deviceSpecificExpiry = { month: x.dsnExp.month, year: x.dsnExp.year }; }
    card.paymentAccountReference = x.par;
    if (op === 'TOKEN') card.storedOnFile = 'STORED';
    var sof = { type: nt ? 'SCHEME_TOKEN' : 'CARD' };
    if (op === 'TOKEN') sof.token = D.mpgsToken(b);
    sof.provided = { card: card };
    return { result: 'SUCCESS', response: { gatewayCode: 'APPROVED', acquirerCode: '00' }, sourceOfFunds: sof };
  };
  D.cybsResp = function (b, nt) {
    var x = D.brand[b];
    var r = { status: 'AUTHORIZED', processorInformation: { responseCode: '00', paymentAccountReferenceNumber: x.par } };
    if (nt) {
      r.processingInformation = { paymentSolution: x.ps };
      r.paymentInformation = { card: { bin: x.tokenBin } };
    }
    return r;
  };

  /* Pretty JSON with optional highlighted keys (dot paths). */
  D.json = function (obj, hl) {
    hl = hl || [];
    var esc = function (s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
    function walk(v, path, ind) {
      var pad = new Array(ind + 1).join('  ');
      if (v === null) return '<span class="cm">null</span>';
      if (typeof v !== 'object') return typeof v === 'string' ? '"' + esc(v) + '"' : esc(v);
      var keys = Object.keys(v);
      if (!keys.length) return '{}';
      var out = keys.map(function (k) {
        var p = path ? path + '.' + k : k;
        var val = walk(v[k], p, ind + 1);
        var line = '"' + esc(k) + '": ' + val;
        if (hl.indexOf(p) >= 0) line = '<span class="hl">' + line + '</span>';
        return pad + '  ' + line;
      });
      return '{\n' + out.join(',\n') + '\n' + pad + '}';
    }
    return walk(obj, '', 0);
  };
  window.NT = D;
})();
